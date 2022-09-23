export default function ({store}) {
    store.dispatch('updateDiscordMemberCount');
    store.dispatch('updatePlayerCount');
    store.dispatch('loadTransactionHistory');
    store.dispatch('updateTransactionStatuses');
}
