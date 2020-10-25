/*
 *              Ineractive access to suboptimal folding
 *
 *                         c Ivo L Hofacker
 *                        Vienna RNA package
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <config.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
#include "ViennaRNA/part_func.h"
#include "ViennaRNA/fold.h"
#include "ViennaRNA/cofold.h"
#include "ViennaRNA/fold_vars.h"
#include "ViennaRNA/utils.h"
#include "ViennaRNA/read_epars.h"
#include "ViennaRNA/subopt.h"
#include "ViennaRNA/params.h"
#include "ViennaRNA/constraints.h"
#include "ViennaRNA/constraints_SHAPE.h"
#include "ViennaRNA/file_formats.h"
#include "RNAsubopt_cmdl.h"
#include "gengetopt_helper.h"
#include "input_id_helper.h"

#include "ViennaRNA/color_output.inc"

PRIVATE void putoutzuker(vrna_subopt_solution_t *zukersolution);


int
main(int  argc,
     char *argv[])
{
  struct          RNAsubopt_args_info args_info;
  char                                fname[FILENAME_MAX_LENGTH], *rec_sequence, *rec_id,
                                      **rec_rest, *orig_sequence, *constraints_file, *cstruc, *structure,
                                      *shape_file, *shape_method, *shape_conversion;
  unsigned int                        rec_type, read_opt;
  int                                 i, length, cl, istty, delta, n_back, noconv, dos, zuker, with_shapes,
                                      verbose, enforceConstraints, st_back_en, batch;
  double                              deltap;
  vrna_md_t                           md;

  do_backtrack  = 1;
  delta         = 100;
  deltap        = n_back = noconv = dos = zuker = 0;
  rec_type      = read_opt = 0;
  rec_id        = rec_sequence = orig_sequence = NULL;
  rec_rest      = NULL;
  cstruc        = structure = NULL;
  verbose       = 0;
  st_back_en    = 0;

  set_model_details(&md);

  /* switch on unique multibranch loop decomposition */
  md.uniq_ML = 1;

  /*
   #############################################
   # check the command line parameters
   #############################################
   */
  if (RNAsubopt_cmdline_parser(argc, argv, &args_info) != 0)
    exit(1);

  /* get basic set of model details */
  ggo_get_md_eval(args_info, md);
  ggo_get_md_fold(args_info, md);
  ggo_get_md_part(args_info, md);
  ggo_get_circ(args_info, md.circ);

  /* check dangle model */
  if ((md.dangles < 0) || (md.dangles > 3)) {
    vrna_message_warning("required dangle model not implemented, falling back to default dangles=2");
    md.dangles = dangles = 2;
  }

  /* SHAPE reactivity data */
  ggo_get_SHAPE(args_info, with_shapes, shape_file, shape_method, shape_conversion);

  ggo_get_constraints_settings(args_info,
                               fold_constrained,
                               constraints_file,
                               enforceConstraints,
                               batch);

  if (args_info.verbose_given)
    verbose = 1;

  /* enforce canonical base pairs in any case? */
  if (args_info.canonicalBPonly_given)
    md.canonicalBPonly = canonicalBPonly = 1;

  /* do not convert DNA nucleotide "T" to appropriate RNA "U" */
  if (args_info.noconv_given)
    noconv = 1;

  /* energy range */
  if (args_info.deltaEnergy_given)
    delta = (int)(0.1 + args_info.deltaEnergy_arg * 100);

  /* energy range after post evaluation */
  if (args_info.deltaEnergyPost_given)
    deltap = args_info.deltaEnergyPost_arg;

  /* sorted output */
  if (args_info.sorted_given)
    subopt_sorted = 1;

  /* stochastic backtracking */
  if (args_info.stochBT_given) {
    n_back = args_info.stochBT_arg;
    vrna_init_rand();
    md.compute_bpp = 0;
  }

  if (args_info.stochBT_en_given) {
    n_back          = args_info.stochBT_en_arg;
    st_back_en      = 1;
    md.compute_bpp  = 0;
    vrna_init_rand();
  }

  /* density of states */
  if (args_info.dos_given) {
    dos           = 1;
    print_energy  = -999999;
  }

  /* logarithmic multiloop energies */
  if (args_info.logML_given)
    md.logML = logML = 1;

  /* zuker subopts */
  if (args_info.zuker_given)
    zuker = 1;

  if (zuker) {
    if (md.circ) {
      vrna_message_warning("Sorry, zuker subopts not yet implemented for circfold");
      RNAsubopt_cmdline_parser_print_help();
      exit(1);
    } else if (n_back > 0) {
      vrna_message_warning("Can't do zuker subopts and stochastic subopts at the same time");
      RNAsubopt_cmdline_parser_print_help();
      exit(1);
    } else if (md.gquad) {
      vrna_message_warning("G-quadruplex support for Zuker subopts not implemented yet");
      RNAsubopt_cmdline_parser_print_help();
      exit(1);
    }
  }

  if (md.gquad && (n_back > 0)) {
    vrna_message_warning("G-quadruplex support for stochastic backtracking not implemented yet");
    RNAsubopt_cmdline_parser_print_help();
    exit(1);
  }

  /* free allocated memory of command line data structure */
  RNAsubopt_cmdline_parser_free(&args_info);

  /*
   #############################################
   # begin initializing
   #############################################
   */

  istty = isatty(fileno(stdout)) && isatty(fileno(stdin));

  /* print user help if we get input from tty */
  if (istty) {
    if (!zuker)
      print_comment(stdout, "Use '&' to connect 2 sequences that shall form a complex.");

    if (fold_constrained) {
      vrna_message_constraint_options(VRNA_CONSTRAINT_DB_DOT | VRNA_CONSTRAINT_DB_X | VRNA_CONSTRAINT_DB_ANG_BRACK | VRNA_CONSTRAINT_DB_RND_BRACK);
      vrna_message_input_seq("Input sequence (upper or lower case) followed by structure constraint");
    } else {
      vrna_message_input_seq_simple();
    }
  }

  /* set options we wanna pass to vrna_file_fasta_read_record() */
  if (istty)
    read_opt |= VRNA_INPUT_NOSKIP_BLANK_LINES;

  if (!fold_constrained)
    read_opt |= VRNA_INPUT_NO_REST;

  /*
   #############################################
   # main loop: continue until end of file
   #############################################
   */
  while (
    !((rec_type = vrna_file_fasta_read_record(&rec_id, &rec_sequence, &rec_rest, NULL, read_opt))
      & (VRNA_INPUT_ERROR | VRNA_INPUT_QUIT))) {
    /*
     ########################################################
     # init everything according to the data we've read
     ########################################################
     */
    if (rec_id)
      /* if(!istty) printf("%s\n", rec_id); */
      (void)sscanf(rec_id, ">%" XSTR(FILENAME_ID_LENGTH) "s", fname);
    else
      fname[0] = '\0';

    /* convert DNA alphabet to RNA if not explicitely switched off */
    if (!noconv)
      vrna_seq_toRNA(rec_sequence);

    /* store case-unmodified sequence */
    orig_sequence = strdup(rec_sequence);
    /* convert sequence to uppercase letters only */
    vrna_seq_toupper(rec_sequence);

    vrna_fold_compound_t *vc = vrna_fold_compound(rec_sequence, &md, VRNA_OPTION_MFE | (circ ? 0 : VRNA_OPTION_HYBRID) | ((n_back > 0) ? VRNA_OPTION_PF : 0));
    length = vc->length;

    structure = (char *)vrna_alloc((char)length + 1);

    /* parse the rest of the current dataset to obtain a structure constraint */
    if (fold_constrained) {
      if (constraints_file) {
        vrna_constraints_add(vc, constraints_file, VRNA_OPTION_MFE | ((n_back > 0) ? VRNA_OPTION_PF : 0));
      } else {
        cstruc = NULL;
        int           cp        = -1;
        unsigned int  coptions  = (rec_id) ? VRNA_OPTION_MULTILINE : 0;
        cstruc  = vrna_extract_record_rest_structure((const char **)rec_rest, 0, coptions);
        cstruc  = vrna_cut_point_remove(cstruc, &cp);
        if (vc->cutpoint != cp) {
          vrna_message_error("Sequence and Structure have different cut points.\n"
                             "sequence: %d, structure: %d",
                             vc->cutpoint, cp);
        }

        cl = (cstruc) ? (int)strlen(cstruc) : 0;

        if (cl == 0)
          vrna_message_warning("Structure constraint is missing");
        else if (cl < length)
          vrna_message_warning("Structure constraint is shorter than sequence");
        else if (cl > length)
          vrna_message_error("Structure constraint is too long");

        if (cstruc) {
          strncpy(structure, cstruc, sizeof(char) * (cl + 1));

          /* convert pseudo-dot-bracket to actual hard constraints */
          unsigned int constraint_options = VRNA_CONSTRAINT_DB_DEFAULT;

          if (enforceConstraints)
            constraint_options |= VRNA_CONSTRAINT_DB_ENFORCE_BP;

          vrna_constraints_add(vc, (const char *)structure, constraint_options);
        }
      }
    }

    if (with_shapes)
      vrna_constraints_add_SHAPE(vc, shape_file, shape_method, shape_conversion, verbose, VRNA_OPTION_MFE | ((n_back > 0) ? VRNA_OPTION_PF : 0));

    if (istty) {
      if (cut_point == -1)
        vrna_message_info(stdout, "length = %d", length);
      else
        vrna_message_info(stdout, "length1 = %d\nlength2 = %d", cut_point - 1, length - cut_point + 1);
    }

    /*
     ########################################################
     # begin actual computations
     ########################################################
     */

    if ((logML != 0 || md.dangles == 1 || md.dangles == 3) && dos == 0)
      if (deltap <= 0)
        deltap = delta / 100. + 0.001;

    if (deltap > 0)
      print_energy = deltap;

    /* stochastic backtracking */
    if (n_back > 0) {
      double  mfe, kT, ens_en;
      char    *ss;

      if (vc->cutpoint != -1)
        vrna_message_error("Boltzmann sampling for cofolded structures not implemented (yet)!");

      if (fname[0] != '\0')
        print_fasta_header(stdout, fname);

      printf("%s\n", rec_sequence);

      ss = (char *)vrna_alloc(strlen(rec_sequence) + 1);
      strncpy(ss, structure, length);
      mfe = vrna_mfe(vc, ss);
      /* rescale Boltzmann factors according to predicted MFE */
      vrna_exp_params_rescale(vc, &mfe);
      /* ignore return value, we are not interested in the free energy */
      ens_en  = vrna_pf(vc, ss);
      kT      = vc->exp_params->kT;

      free(ss);

      for (i = 0; i < n_back; i++) {
        char *s, *e_string = NULL;
        s = vrna_pbacktrack(vc);
        if (st_back_en) {
          double e, prob;
          e         = vrna_eval_structure(vc, s);
          prob      = exp((ens_en - e) / kT);
          e_string  = vrna_strdup_printf(" %6.2f %6g", e, prob);
        }

        print_structure(stdout, s, e_string);
        free(s);
        free(e_string);
      }
    }
    /* normal subopt */
    else if (!zuker) {
      /* first lines of output (suitable  for sort +1n) */
      if (fname[0] != '\0') {
        char *head = vrna_strdup_printf("%s [%d]", fname, delta);
        print_fasta_header(stdout, head);
        free(head);
      }

      vrna_subopt(vc, delta, subopt_sorted, stdout);

      if (dos) {
        int i;
        for (i = 0; i <= MAXDOS && i <= delta / 10; i++)
          printf("%4d %6d\n", i, density_of_states[i]);
      }
    }
    /* Zuker suboptimals */
    else {
      vrna_subopt_solution_t  *zr;

      if (vc->cutpoint != -1)
        vrna_message_error("Sorry, zuker subopts not yet implemented for cofold");

      int                     i;
      if (fname[0] != '\0')
        print_fasta_header(stdout, fname);

      printf("%s\n", rec_sequence);

      zr = vrna_subopt_zuker(vc);

      putoutzuker(zr);
      (void)fflush(stdout);
      for (i = 0; zr[i].structure; i++)
        free(zr[i].structure);
      free(zr);
    }

    (void)fflush(stdout);

    /* clean up */
    vrna_fold_compound_free(vc);

    if (cstruc)
      free(cstruc);

    if (rec_id)
      free(rec_id);

    free(rec_sequence);
    free(orig_sequence);
    free(structure);

    /* free the rest of current dataset */
    if (rec_rest) {
      for (i = 0; rec_rest[i]; i++)
        free(rec_rest[i]);
      free(rec_rest);
    }

    rec_id    = rec_sequence = orig_sequence = structure = cstruc = NULL;
    rec_rest  = NULL;

    if (with_shapes || (constraints_file && (!batch)))
      break;

    /* print user help for the next round if we get input from tty */
    if (istty) {
      if (!zuker)
        print_comment(stdout, "Use '&' to connect 2 sequences that shall form a complex.");

      if (fold_constrained) {
        vrna_message_constraint_options(VRNA_CONSTRAINT_DB_DOT | VRNA_CONSTRAINT_DB_X | VRNA_CONSTRAINT_DB_ANG_BRACK | VRNA_CONSTRAINT_DB_RND_BRACK);
        vrna_message_input_seq("Input sequence (upper or lower case) followed by structure constraint");
      } else {
        vrna_message_input_seq_simple();
      }
    }
  }

  free(shape_method);
  free(shape_conversion);

  return EXIT_SUCCESS;
}


PRIVATE void
putoutzuker(vrna_subopt_solution_t *zukersolution)
{
  int   i;
  char  *e_string;

  for (i = 0; zukersolution[i].structure; i++) {
    e_string = vrna_strdup_printf(" [%6.2f]", zukersolution[i].energy);
    print_structure(stdout, zukersolution[i].structure, e_string);
    free(e_string);
  }
  return;
}
