const fs = require("fs");

const verifiers = [ // Old file name, new file name, contract name
                    ["verifier.sol", "MinAgeVerifier.sol", "MinAgeVerifier"]
                  ];

return Promise.all(verifiers.map(async (verifier) => {
    const oldFileName = verifier[0];
    const newFileName = verifier[1];
    const contractName = verifier[2];

    let file = await fs.readFileSync(__dirname + "/../../verifier/" + oldFileName, "utf8");
    file = file.replace(/contract Verifier {/, "contract " + contractName + " {");
    fs.writeFileSync(__dirname + "/../contracts/" + newFileName, file);
}));