import os
import json
import argparse

from datetime import datetime, timezone

from jinja2.loaders import FileSystemLoader

from pluginparser import PluginParser
from models.dmxcversion import DMXCVersion

from jinja2 import Environment, select_autoescape


def main(infolder: str, outfolder: str, url: str, verbose: bool):
    parser = PluginParser(infolder)

    if not os.path.exists(os.path.join(outfolder, "plugins")):
        os.mkdir(os.path.join(outfolder, "plugins"))
    print("Parsing plugins...")

    versions = dict()

    for plugin, file in parser.getpluginsfile():
        if verbose:
            print(f"Parsing {file}")
        for version in plugin.versions:
            for v in version.dmxcversion:
                if plugin.checkversion(v):
                    if v not in versions:
                        versions[v] = []
                    append = plugin.toshortdict()
                    append["details"] = url+"/plugins/"+os.path.basename(file)
                    versions[v].append(append)
        with open(file, "r") as infile:
            with open(os.path.join(outfolder, "plugins", os.path.basename(file)), "w") as outfile:
                outfile.write(infile.read())

    if verbose:
        print("Writing output files")

    version = []
    htmldata = []
    for ver in versions:
        timestamp = datetime.now(timezone.utc).isoformat()
        version.append({"version": ver.name, "timestamp": timestamp})
        output = {"version": ver.name, "timestamp": timestamp,
                  "plugins": [plugin for plugin in versions[ver]]}
        htmldata.append(
            {"version": ver, "timestamp": timestamp, "plugins": len(output["plugins"])})
        with open(os.path.join(outfolder, f"{ver.name}.json"), "w") as out:
            if verbose:
                print(f"Writing {os.path.join(outfolder, f'{ver.name}.json')}")
            json.dump(output, out)
    with open(os.path.join(outfolder, "versions.json"), "w") as out:
        json.dump(version, out)

    env = Environment(
        loader=FileSystemLoader("scripts/template"),
        autoescape=select_autoescape()
    )

    with open(os.path.join(outfolder, "index.html"), "w") as out:
        out.write(env.get_template("index.html").render(htmldata=sorted(htmldata, key=lambda x: x["version"])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DMXC Plugin Lib preprocessor.")
    parser.add_argument("infolder", type=str,
                        help="Folder containing the json files for the plugins.")
    parser.add_argument("outfolder", type=str,
                        help="Outputfolder were to write the processed json files.")
    parser.add_argument("baseurl", type=str,
                        help="Url pointing to the github page where the output files are hosted.")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose output.")
    args = parser.parse_args()
    infold = args.infolder
    outfold = args.outfolder
    url = args.baseurl
    main(infold, outfold, url, args.verbose)
