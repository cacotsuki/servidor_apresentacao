%{
/** @file version.i.in
 * @brief Set $RNA::VERSION to the bindings version
 */
%}

%perlcode %{
our $VERSION = '2.3.3';
sub VERSION () { $VERSION };
%}

