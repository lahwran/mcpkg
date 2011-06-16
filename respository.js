// this file is valid javascript but not valid json
// remove the comments to make it valid json
// respositories will be parsed as json
{
    "UpdateTime": unixtime,
    "Packages":
    [
        "package_identifier":
        {
            "Nicename": "Nicer Name",
            "Tags": ["tag1", "tag2"],
            "Screenshots": ["URL1","URL2","URLX"],
            "Author": ["name", "contact"],
            "Packager": ["name", "contact"],
            "Homepage": "URL",
            "Section": "SectionName",
            "Version": "VersionNumber",
            "Source": "URLToSourceCode",
            "Depends": ["package_identifier>=version", "package_identifier==version"],
            "Recommends": ["package_identifier<=version", "package_identifier<<version"],
            "Suggests": ["package_identifier>>version", "package_identifier!=version"],
            "Enhances": ["package_identifier>=version", "package_identifier==version"],
            "Conflicts": ["package_identifier>=version", "package_identifier==version"],
            "Provides": ["package_identifier>=version", "package_identifier==version"],
            "Description": "WOOHOO I LOVE DESCRIPTIONS!"
        }
    ],
    "Sections":
    [
        "SectionName", //name of section - no descriptions (for now?)
        "Stupid mods",
        "Awesome mods",
        "Another section"
    ],
    "Links":
    [
        "URL":
        {
            "Subrepos": bool, // are subrepos grabbed/parsed/added or ignored
            "Sections": bool  // are sections added
        },
        "http://friend1.com/mcpkgrepository":
        {
            "Subrepos": false,
            "Sections": true
        },
        "http://coolguy2.net/otherrepo":
        {
            "Subrepos": true,
            "Sections": true
        }
    ]
}
