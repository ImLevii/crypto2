<template>
	<div class="uk-container uk-margin">
		<div class="transaction-page">
			<div class="transaction uk-animation-fade">
				<span class="section-title" style="text-align: left">Your Transaction</span>
				<span class="section-subtitle" style="text-align: left">#{{ transaction['id'] }}</span>

				<div class="uk-grid uk-margin">
					<div class="uk-width-1-2@m">
						<div class="transaction-details">
							<span class="field-label">You send</span>
							<span class="tx-amount">{{ transaction['crypto_amount'] }} {{ transaction['currency'] }}</span>
							<span class="cx-details">{{ getCurrencyName }}</span>
						</div>
					</div>
					<div class="uk-width-1-2@m">
						<div class="transaction-details">
							<span class="field-label">You receive</span>
							<span class="tx-amount">{{ getReceiveAmount }} USD</span>
							<span class="cx-details">Store Credit</span>
						</div>
					</div>
				</div>

				<hr/>

				<div class="transaction-details">
					<span class="field-label">Exchange rate</span>
					<span class="exchange-rate">{{ transaction['exchange_rate'] }} {{ transaction['currency'] }} = 1 USD</span>
				</div>

				<hr/>

				<div class="uk-grid">
					<div class="uk-width-1-2@m">
						<div class="transaction-details">
							<span class="field-label">Received funds</span>
							<span class="tx-amount" v-if="isAwaitingFunds">Awaiting funds...</span>
							<DateDisplay :timestamp="transaction['last_updated']" class="tx-amount" v-else/>
						</div>
					</div>
					<div class="uk-width-1-2@m">
						<div class="transaction-details" v-if="isAwaitingConfirmations || isPaymentComplete">
							<span class="field-label">Confirmations</span>
							<span class="tx-amount" v-if="isAwaitingConfirmations">{{ transaction['confirmations_needed'] }} remaining...</span>
							<span class="tx-amount" v-else>Payment confirmed</span>
						</div>
					</div>
				</div>

				<template v-if="isAwaitingFunds">
					<div class="payment-instructions uk-margin">
						<div class="transaction-details">
							<span class="field-label">You send</span>
							<span class="tx-amount">{{ transaction['crypto_amount'] }} {{ transaction['currency'] }}</span>
						</div>

						<div class="transaction-details uk-margin-s" style="position: relative">
							<span class="field-label">To payment address</span>

							<button type="button" class="payment-address">
								<i class="fas fa-copy"></i>
								{{ transaction['receiving_address'] }}
							</button>
						</div>

						<img class="qr-code uk-margin" :src="transaction['qr_code_url']" alt="Scan QR Code to Pay"/>

						<p class="important-notice uk-margin">Please send the exact amount from your wallet or exchange account to the payment address.</p>
					</div>
				</template>

				<template v-if="isPaymentComplete">
					<hr/>

					<div class="transaction-details">
						<span class="field-label">Your store credit</span>

						<span class="gift-card uk-margin-s" v-if="this.showingGiftCard">{{ transaction['gift_card'] || 'UNKNOWN' }}</span>

						<button type="button" class="flat-button uk-btn-green alt uk-margin-s" @click="toggleGiftCard()" v-if="!this.showingGiftCard">Show Gift Card</button>
						<button type="button" class="flat-button uk-btn-grey uk-margin-s" @click="toggleGiftCard()" v-else>Hide Gift Card</button>
					</div>
				</template>
			</div>
		</div>
	</div>
</template>

<style scoped>
	.transaction-page {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 40px 0 20px 0;
	}

	.transaction .transaction-details {
		display: flex;
		flex-direction: column;
	}

	.transaction .transaction-details .field-label {
		color: #bbb;
		font-size: 14px;
		line-height: 14px;
	}

	.transaction .transaction-details .tx-amount {
		color: #fff;
		font-size: 18px;
		font-weight: bold;
		line-height: 18px;
		margin: 6px 0;
	}

	.transaction .transaction-details .cx-details {
		color: #69cf54;
		font-size: 14px;
		line-height: 14px;
		text-transform: lowercase;
	}

	.transaction .transaction-details .payment-address {
		color: #69cf54;
		font-size: 14px;
		line-height: 17px;
		text-transform: lowercase;
		text-align: left;
		margin: 3px 0;
	}

	.transaction .transaction-details .payment-address i {
		font-size: 12px;
	}

	.transaction .transaction-details .exchange-rate {
		color: #69cf54;
		font-weight: bold;
	}

	.transaction .transaction-details .gift-card {
		padding: 14px;
		background: #292B35;
		border: none;
		border-radius: 3px;
		color: #fff;
		font-family: 'Rajdhani', sans-serif;
		font-size: 18px;
		font-weight: bold;
		text-align: center;
	}

	.transaction .payment-instructions .qr-code {
		width: 150px;
		height: 150px;
		margin: 10px auto 0 auto;
	}

	.transaction hr {
		border-top-color: #2a262e;
		border-top-width: 2px;
	}

	.transaction {
		position: relative;
		display: flex;
		flex-direction: column;
		width: 460px;
		padding: 30px 40px;
		background: #1c1821;
		border-radius: 8px;
		box-shadow: rgba(0, 0, 0, 0.1) 0 4px 14px;
	}

	.transaction .section-title,
	.transaction .section-subtitle {
		color: #FFF;
		font-family: 'Rajdhani', sans-serif;
		opacity: 0.99;
	}

	.transaction .section-title {
		font-size: 24px;
		font-weight: bold;
		text-transform: uppercase;
		line-height: 24px;
	}

	.transaction .section-subtitle {
		font-size: 14px;
		text-transform: uppercase;
		line-height: 14px;
	}

	.transaction .payment-instructions {
		display: flex;
		flex-direction: column;
		padding: 14px;
		background: #16131A;
		border: none;
		border-radius: 6px;
	}

	.transaction .payment-instructions .important-notice {
		font-size: 12px;
		line-height: 13px;
		color: #bbb;
	}

	@media screen and (max-width: 768px) {

	}
</style>

<script>
	export default {
	    layout: 'dark',
		async asyncData({$axios, route, error}) {
	        const txId = route.params.id;

	        return await $axios.get('/store/tx/info?tx_id=' + txId)
				.then(response => {
				    if (response.status === 200) {
				        return {
				            transaction: response.data
						}
					} else {
						throw 'Unexpected response status';
					}
				})
				.catch(thrown => {
				    if (thrown.response) {
				        if (thrown.response.statusCode === 404) {
	            			error({ statusCode: 404, message: 'Couldn\'t find that transaction' });
						} else {
				            error({ statusCode: thrown.response.statusCode, message: thrown.response.data })
						}
					}
				});
		},
		head() {
	        return {
	            title: 'Your Transaction'
			}
		},
		data() {
	        return {
	            showingGiftCard: false,
	            updatingTask: null,
			}
		},
		mounted() {
	        let ins = this;
	        this.updatingTask = setInterval(function() {
	            if (ins.transaction['tx_status'] === 'PAYMENT_COMPLETE') {
	                clearInterval(ins.updatingTask);
	                ins.updatingTask = null;
	                return;
				}

	            ins.fetchTransactionInfo();
			}, 25000);
        },
		beforeDestroy() {
            this.destroyed = true;

            if (this.updatingTask != null) {
                clearInterval(this.updatingTask);
            }
        },
        methods: {
	        async fetchTransactionInfo() {
	            return await this.$axios.get('/store/tx/info?tx_id=' + this.transaction['id'])
					.then(response => {
						if (response.status === 200) {
							this.transaction = response.data;
						} else {
							throw 'Unexpected response status';
						}
					})
					.catch(thrown => {
						if (thrown.response) {
							if (thrown.response.statusCode === 404) {
								error({ statusCode: 404, message: 'Couldn\'t find that transaction' });
							} else {
								error({ statusCode: thrown.response.statusCode, message: thrown.response.data })
							}
						}
					});
			},
	        toggleGiftCard() {
	            this.showingGiftCard = !this.showingGiftCard;
			},
		},
		computed: {
	        getCurrencyName: function() {
	            switch (this.transaction['currency']) {
	                case 'BTC':
	                    return 'Bitcoin';
	                case 'ETH':
	                    return 'Ethereum';
	                case 'XRP':
	                    return 'Ripple';
	                case 'XMR':
	                    return 'Monero';
	                case 'BNB':
	                    return 'Binance';
	                case 'LTC':
	                    return 'Litecoin';
					case 'DOGE':
					    return 'Dogecoin';
					case 'USDT':
					    return 'Tether';
				}
			},
	        getReceiveAmount: function() {
	            return Math.round(((this.transaction['crypto_amount'] / this.transaction['exchange_rate']) + Number.EPSILON) * 100) / 100;
			},
			isAwaitingFunds: function() {
	            return this.transaction['tx_status'] === 'AWAITING_PAYMENT';
			},
			isAwaitingConfirmations: function() {
	            return this.transaction['tx_status'] === 'AWAITING_CONFIRMATIONS';
			},
			isPaymentComplete: function() {
	            return this.transaction['tx_status'] === 'PAYMENT_COMPLETE';
			},
		}
	}
</script>
