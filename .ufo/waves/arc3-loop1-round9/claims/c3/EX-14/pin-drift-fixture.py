from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory

repo = Path(__file__).resolve().parents[6]
spec = spec_from_file_location("census", repo / ".ufo/gates/c1-census-v10.py")
census = module_from_spec(spec)
spec.loader.exec_module(census)

with TemporaryDirectory(dir="/var/tmp", prefix="kaidoku-ex14-") as scratch:
    config = Path(scratch) / ".kimi-code" / "config.toml"
    config.parent.mkdir(parents=True)
    stanza = '[mcp_servers.rea]\nargs = [ "-y", "rea-agents@6.7.0", "mcp" ]\n'
    config.write_text(stanza)
    live = {"kimi": "6.7.0"}
    print("fixture baseline line 2:", census.ptr_check(str(config), 2, live))
    config.write_text("\n" + stanza)
    print("after adding a leading blank line, old line 2:", census.ptr_check(str(config), 2, live))
    print("after adding a leading blank line, re-anchored line 3:", census.ptr_check(str(config), 3, live))
