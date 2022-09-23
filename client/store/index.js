const SERVER_ADDRESS = 'play.hcrivals.org';
const DISCORD_GUILD_ID = '';

export const state = () => ({
	discordMemberCount: 0,
    playerCount: 0,
    transactions: {}
});

export const mutations = {
    setDiscordMemberCount(state, n) {
	    state.discordMemberCount = n;
    },
	setPlayerCount(state, n) {
		state.playerCount = n;
	},
    setTransactions(state, txStates) {
        state.transactions = txStates;
    },
    addTransaction(state, transaction) {
        if (state.transactions.length > 10) {
            let oldestTransaction = null;

            for (const transaction in state.transactions) {
                if (typeof transaction !== 'object') {
                    continue
                }

                if (oldestTransaction == null) {
                    oldestTransaction = transaction;
                } else if (transaction.createdAt < oldestTransaction.createdAt) {
                    oldestTransaction = transaction;
                }
            }
        }

        state.transactions[transaction.id] = transaction;
    },
    saveTransactionHistory(state) {
	    localStorage.setItem('TransactionHistory', JSON.stringify(state.transactions))
    },
    updateTransactionState(state, transaction) {
        state.transactions[transaction.id] = transaction;
    }
};

export const actions = {
	async updateDiscordMemberCount({commit}) {
	    const memberCount = await this.$axios.get('https://discordapp.com/api/guilds/' + DISCORD_GUILD_ID + '/embed.json').then(result => {
            return result.data.presence_count;
        });

		commit('setDiscordMemberCount', memberCount);
	},
    async updatePlayerCount({commit}) {
	     const playerCount = await this.$axios.get('https://mcapi.us/server/status?ip=' + SERVER_ADDRESS).then(result => {
            if (result.data.status === 'success' && result.data.online) {
                return result.data.players.now;
            } else {
                return 0;
            }
        });

        commit('setPlayerCount', playerCount);
    },
    loadTransactionHistory({commit}) {
        const localData = localStorage.getItem('TransactionHistory');
        if (localData != null) {
            commit('setTransactions', JSON.parse(localData));
        }
    },
    updateTransactionStatuses({state, commit}) {
	    if (typeof state.transactions !== 'object') {
	        return;
        }

	    if (Object.keys(state.transactions).length <= 1) {
	        return;
        }

	    const txIds = [];
	    Object.keys(state.transactions).forEach(key => {
	        txIds.push(state.transactions[key].id);
        });

	    if (txIds.length <= 0) {
	        return;
        }

	    this.$axios.post('/store/tx/info', {'tx_ids': txIds}).then(response => {
	        if (response.status === 200) {
	            response.data.forEach(function(transaction) {
                    if (transaction.id in state.transactions) {
                        commit('updateTransactionState', transaction);
                    }
                });
            }
        }).catch(error => {
            console.log('error updating tx statuses');
            console.log(error);
        });
    }
};

export const getters = {
	getDiscordMemberCount: state => {
		return state.discordMemberCount;
	},
	getPlayerCount: state => {
		return state.playerCount;
	},
    getTransactions: state => {
	    return state.transactions;
    },
    getSortedTransactions: state => {
	    const transactions = [];

	    Object.keys(state.transactions).forEach(function (txId) {
	        transactions.push(state.transactions[txId]);
        });

	    transactions.sort(function (t1, t2) {
	        return t2.created_at - t1.created_at;
        });

	    return transactions;
    }
};
