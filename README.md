# Linear-vesting
Contrat de vesting linéaire créé avec Solidity pour la blockchain Ethereum. Le contrat permet à un propriétaire de tokens ERC20 de les verrouiller dans le contrat pour une période de temps spécifiée, après laquelle les tokens sont progressivement libérés à un bénéficiaire sur une durée définie.

Le contrat démarre avec une période de "cliff", pendant laquelle aucune allocation n'est libérée.

Après la période de cliff, les tokens sont libérés de manière linéaire sur la période de vesting.
