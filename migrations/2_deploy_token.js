const MyToken = artifacts.require("MyToken");

module.exports = function (deployer) {
    // Déployez le contrat et donnez toute l'offre initiale à l'adresse de déploiement
    deployer.deploy(MyToken, "1000000000000000000000");
};
