# Build the canonical manuscript from the repository root.
$out_dir = 'build';

# LuaLaTeX loads OpenType fonts through luaotfload, which needs writable
# cache directories.  Keep them in the ignored repository runtime area so
# editor builds do not depend on a user-level TeX cache being available.
use File::Path qw(make_path);
use Cwd qw(abs_path);
make_path('.agent-runtime/tex-cache/var');
make_path('.agent-runtime/tex-cache/cache');
$ENV{'TEXMFCACHE'} = abs_path('.agent-runtime/tex-cache/var');
$ENV{'LUOTFLOAD_CACHE'} = abs_path('.agent-runtime/tex-cache/cache');
