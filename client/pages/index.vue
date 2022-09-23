<template>
  <div class="uk-container uk-margin">
    <div class="hero">
      <div class="hero-text mobile-only">
        <span class="hero-title">Purchase using crypto.</span>
        <span class="hero-paragraph">A fast and secure way to purchase anything on our store using {{ getSupportedCurrenciesNum }} popular cryptocurrencies. Fully automated with no verification required.</span>

        <ul class="crypto-list">
          <li v-for="currency in currencies">
            <img :src="currency.icon" :alt="currency.name">
          </li>
        </ul>

        <div v-if="isExtraCreditEnabled" class="sale-or-discount sale uk-margin">
          <span class="page-title">Ongoing Sale</span>
          <span class="info">Get {{ getExtraCreditPercentage }}% extra gift-card credit!</span>
        </div>
      </div>

      <form v-if="!confirming" class="purchase-form uk-animation-fade">
        <span class="form-title">Exchange Crypto</span>
        <span class="form-subtitle">For store credit</span>

        <p v-if="error != null" class="uk-p uk-p-red uk-margin">
          {{ error }}
        </p>
        <p v-if="updated" class="uk-p uk-p-yellow uk-margin">
          The exchange rate has updated! Check the exchange
          details and try again.
        </p>

        <div class="uk-form-controls uk-margin uk-form-group">
          <span class="uk-input-label">You send</span>

          <label>
            <input
              v-model="youSendAmount"
              class="uk-input"
              type="number"
              step="any"
              @change="onUpdateSendAmount"
            >
          </label>

          <button class="currency-dropdown-btn" type="button">
            <span class="currency-info">
              <span class="name">{{ currencyName }}</span>
              <span class="tag">{{ currencyTag }}</span>
            </span>

            <i class="fas fa-angle-down" />
          </button>

          <div ref="currency-dropdown" uk-dropdown="mode: click; pos: bottom-right" class="currency-dropdown">
            <ul>
              <li v-for="currency in currencies">
                <a @click="selectCurrency(currency)">
                  <img :src="currency.icon" :alt="currency.tag">
                  <span class="currency-tag">{{ currency.tag }}</span>
                  <span class="currency-name">{{ currency.name }}</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div class="uk-form-controls uk-margin uk-form-group">
          <label>
            <span class="uk-input-label">You receive approximately</span>
            <input v-model="youReceiveAmount" class="uk-input" type="number" @change="onUpdateReceiveAmount">

            <div class="currency-conversion">
              <span class="name">Store Credit</span>
              <span class="tag">USD</span>
            </div>
          </label>
        </div>
        <div class="uk-form-controls uk-margin">
          <label>
            <input v-model="buyerEmail" class="uk-input" type="email" placeholder="Your email address">
          </label>
        </div>
        <div class="uk-form-controls uk-margin">
          <button
            class="flat-button uk-btn-green"
            type="submit"
            :disabled="updating"
            @click.stop.prevent="startPurchase()"
          >
            Exchange now
          </button>
        </div>
      </form>

      <form v-else class="purchase-form uk-animation-fade">
        <span class="form-title" style="text-align: left">Checkout</span>

        <button type="button" class="back-button" @click="goBack()">
          <i class="fas fa-arrow-alt-left" />
          Back
        </button>

        <p v-if="error != null" class="uk-p uk-p-red alt uk-margin">
          {{ error }}
        </p>
        <p v-if="updated" class="uk-p uk-p-yellow alt uk-margin">
          The exchange rate has updated! Check your
          checkout details and try again.
        </p>

        <div class="uk-grid uk-margin">
          <div class="uk-width-1-2@m">
            <div class="transaction-details">
              <span class="field-label">You send</span>
              <span class="tx-amount">{{ youSendAmount }} {{ currencyTag }}</span>
              <span class="cx-details">{{ currencyName }}</span>
            </div>
          </div>
          <div class="uk-width-1-2@m">
            <div class="transaction-details">
              <span class="field-label">You get</span>
              <span class="tx-amount">{{ youReceiveAmount }} USD</span>
              <span class="cx-details">Store Credit</span>
            </div>
          </div>
        </div>

        <hr>

        <div class="transaction-details">
          <span class="field-label">Guaranteed rate</span>
          <span class="exchange-rate">1 {{ currencyTag }} = {{ currencyRate }} USD</span>
        </div>

        <div class="uk-form-controls uk-margin">
          <button
            class="flat-button uk-btn-green"
            type="submit"
            :disabled="updating"
            @click.stop.prevent="confirmPurchase()"
          >
            Checkout
          </button>
        </div>
      </form>

      <div class="hero-text">
        <span class="hero-title">Purchase using crypto.</span>
        <span class="hero-paragraph">A fast and secure way to purchase anything on our store using {{ getSupportedCurrenciesNum }} popular cryptocurrencies. Fully automated with no verification required.</span>

        <ul class="crypto-list">
          <li v-for="currency in currencies">
            <img :src="currency.icon" :alt="currency.name">
          </li>
        </ul>

        <div v-if="isExtraCreditEnabled" class="sale-or-discount sale uk-margin">
          <span class="page-title">Ongoing Sale</span>
          <span class="info">Get {{ getExtraCreditPercentage }}% extra gift-card credit!</span>
        </div>
      </div>
    </div>
    <div class="uk-margin">
      <span class="page-title">Transaction History</span>

      <table class="uk-table transaction-history">
        <thead>
          <tr>
            <th>Order #</th>
            <th>You Pay</th>
            <th>You Get</th>
            <th>Status</th>
            <th>Date</th>
            <th />
          </tr>
        </thead>
        <tbody>
          <tr v-if="Object.keys($store.getters['getTransactions']).length <= 0">
            <td colspan="6" class="no-history">
              You have no transaction history...
            </td>
          </tr>
          <template v-else>
            <tr v-for="transaction in $store.getters['getSortedTransactions']">
              <td>{{ transaction.id }}</td>
              <td><img class="crypto" :src="getCurrencyIcon(transaction.currency)" :alt="transaction.currency"> {{ transaction.crypto_amount }} {{ transaction.currency }}</td>
              <td>${{ Math.round(((transaction.crypto_amount / transaction.exchange_rate) + Number.EPSILON) * 100) / 100 }}</td>
              <td>
                <span v-if="transaction.tx_status === 'PAYMENT_COMPLETE'" class="payment-status completed">Completed</span>
                <span v-if="transaction.tx_status === 'AWAITING_PAYMENT'" class="payment-status awaiting_payment">Awaiting Payment</span>
                <span v-if="transaction.tx_status === 'AWAITING_CONFIRMATIONS'" class="payment-status awaiting_confirmations">Awaiting Confirmations</span>
                <span v-if="transaction.tx_status === 'CANCELLED'" class="payment-status cancelled">Cancelled</span>
              </td>
              <td>
                <DateDisplay :timestamp="transaction.created_at" />
              </td>
              <td>
                <nuxt-link :to="{ name: 'transaction-id', params: { id: transaction.id } }" class="flat-button small uk-btn-blue">
                  <i class="fas fa-eye" />
                </nuxt-link>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.transaction-history {
  margin-top: 10px;
  padding: 30px 40px;
  background: #21272C;
  border-radius: 5px;
  box-shadow: 0 10px 12px rgba(0, 0, 0, 0.1);
}

.transaction-history thead th {
  font-weight: bold;
  text-transform: uppercase;
}

.transaction-history tbody td.no-history {
  padding: 20px;
}

.transaction-history tbody td:first-child {
  padding: 20px 12px 20px 20px;
}

.transaction-history tbody td:last-child {
  padding: 20px 20px 20px 12px;
}

.transaction-history tbody tr:nth-child(odd) {
  background: #2C3136;
}

.transaction-history tbody tr:nth-child(even) {
  background: #32373c;
}

.transaction-history tbody td {
  color: #fff;
  line-height: 16px;
}

.transaction-history tbody td img.crypto {
  display: inline-block;
  width: 16px;
  height: 16px;
  line-height: 16px;
}

.sale-or-discount {
  display: flex;
  align-items: center;
}

.sale-or-discount .page-title {
  display: inline-block;
  flex-shrink: 0;
  height: 30px;
  padding: 6px 14px;
  margin: 0;
  border-radius: 3px 0 0 3px;
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  line-height: 18px;
  letter-spacing: 1px;
  text-decoration: none;
  text-transform: uppercase;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.sale-or-discount.sale .page-title {
  background-color: #fe3c45;
  border-bottom: 2px solid #d2353d;
}

.sale-or-discount .info {
  height: 30px;
  flex-grow: 1;
  padding: 3px 14px;
  background-color: #2C3136;
  border-bottom: 2px solid #22272c;
  border-radius: 0 3px 3px 0;
  color: #fff;
  font-size: 15px;
  font-weight: bold;
}

.payment-status {
  padding: 3px 12px;
  border: 1px solid rgba(5, 5, 5, 0.19);
  border-radius: 3px;
  font-size: 12px;
  font-weight: bold;
  text-shadow: 0 1px 1px rgba(5, 5, 5, 0.19);
}

.payment-status.awaiting_payment {
  background-color: #0f6ecd;
  color: #fff;
}

.payment-status.awaiting_confirmations {
  background-color: #e9cc07;
  color: #fff;
}

.payment-status.completed {
  background-color: #1ecd21;
  color: #fff;
}

.payment-status.cancelled {
  background-color: #bf1918;
  color: #fff;
}

.brand {
  width: 100%;
}

.brand img {
  display: block;
  width: 500px;
  height: 225px;
  max-width: none;
}

.brand .splash-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.brand .splash-section.right {
  text-align: left;
}

.brand .splash-section.left {
  text-align: right;
}

.brand .section-subtitle,
.brand .section-title {
  font-family: "Lato", sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  opacity: 0.99;
}

.brand .section-title {
  color: #fff;
  font-size: 24px;
  text-shadow: 0 1px 1px rgba(5, 5, 5, 0.3);
  line-height: 18px;
}

.brand .section-subtitle {
  margin-top: 2px;
  color: #bbb;
  font-size: 16px;
  text-shadow: 0 1px 1px rgba(5, 5, 5, 0.2);
  line-height: 16px;
}

.brand .section-subtitle,
.brand .section-title {
  font-family: "Lato", sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  opacity: .99;
}

.brand .icon-btn {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: .99;
  color: #fff;
}

.brand .icon-btn i.fa-discord {
  position: relative;
  top: 2px;
  font-size: 42px;
}

.brand .splash-section.left i {
  margin-left: 10px;
}

.brand .splash-section.right i {
  margin-right: 10px;
}

.brand .icon-btn i {
  display: flex;
  align-items: center;
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
  font-size: 40px;
  transition: color .15s ease-in-out, background-color .15s ease-in-out;
}

.brand .copy-popup {
  position: absolute;
  display: none;
  opacity: 0;
  bottom: -30px;
  z-index: 1000;
  width: 300px;
  padding: 6px;
  font-size: 13px;
  line-height: 12px;
}

.hero {
  display: flex;
  padding: 40px 0;
}

.hero-text.mobile-only {
  display: none;
  margin: 0;
}

@media screen and (max-width: 800px) {
  .hero {
    flex-direction: column;
  }

  .hero > div {
    width: 100%;
  }

  .hero-text {
    display: none !important;
  }

  .hero-text.mobile-only {
    display: block !important;
  }
}

.purchase-form .transaction-details {
  display: flex;
  flex-direction: column;
}

.purchase-form .transaction-details .field-label {
  color: #bbb;
  font-size: 14px;
  line-height: 14px;
}

.purchase-form .transaction-details .tx-amount {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  line-height: 18px;
  margin: 6px 0;
}

.purchase-form .transaction-details .cx-details {
  color: #69cf54;
  font-size: 14px;
  line-height: 14px;
  text-transform: lowercase;
}

.purchase-form .transaction-details .exchange-rate {
  color: #69cf54;
  font-weight: bold;
}

.purchase-form hr {
  border-top-color: #2a262e;
  border-top-width: 2px;
}

.purchase-form .back-button {
  position: absolute;
  top: 26px;
  right: 40px;
  padding: 8px 12px;
  background: #2a262e;
  border-radius: 3px;
  color: #fff;
  font-size: 16px;
  font-family: 'Rajdhani', sans-serif;
  font-weight: bold;
  text-transform: uppercase;
  line-height: 15px;
}

.purchase-form .back-button i {
  font-size: 13px;
  margin-right: 4px;
}

.purchase-form {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 460px;
  padding: 30px 40px;
  background: #2C3136;
  border-radius: 8px;
  box-shadow: rgba(0, 0, 0, 0.1) 0 4px 40px;
}

.purchase-form .form-title,
.purchase-form .form-subtitle {
  color: #FFF;
  font-family: 'Rajdhani', sans-serif;
  opacity: 0.99;
}

.purchase-form .form-title {
  color: #fff;
  font-size: 24px;
  font-weight: bold;
  text-transform: uppercase;
  text-align: center;
  line-height: 24px;
}

.purchase-form .form-subtitle {
  color: #bbb;
  font-size: 14px;
  text-transform: uppercase;
  text-align: center;
  line-height: 14px;
}

.purchase-form .uk-form-group {
  position: relative;
}

.purchase-form .uk-form-group .uk-input {
  padding: 40px 14px 20px 14px;
  font-size: 21px;
  font-weight: bold;
  line-height: 16px;
}

.purchase-form .uk-input {
  padding: 20px 14px;
  background: #363b40;
  border: none;
  border-bottom: 2px solid #20262b;
  border-radius: 4px;
  color: #fff;
  font-size: 16px;
  line-height: 13px;
}

.purchase-form .uk-input::placeholder {
  color: #bbb;
}

.purchase-form .uk-input:-ms-input-placeholder {
  color: #bbb;
}

.purchase-form::-ms-input-placeholder {
  color: #bbb;
}

.purchase-form .uk-input:-webkit-autofill,
.purchase-form .uk-input:-webkit-autofill:hover,
.purchase-form .uk-input:-webkit-autofill:focus {
  -webkit-text-fill-color: #fff;
  -webkit-box-shadow: 0 0 0px 1000px #363b40 inset;
  transition: background-color 5000s ease-in-out 0s;
}

.purchase-form .uk-input::-webkit-outer-spin-button,
.purchase-form .uk-input::-webkit-inner-spin-button {
  display: none;
}

.purchase-form .uk-input-label {
  position: absolute;
  top: 10px;
  padding: 0 14px;
  font-size: 13px;
  color: #bbb;
}

.purchase-form .currency-dropdown {
  width: 100%;
  top: 76px !important;
  padding: 10px 0;
  background: #272c31;
  border: none;
  border-radius: 4px;
}

.purchase-form .currency-dropdown ul > li > a {
  display: flex;
  align-items: center;
  padding: 10px 10px;
  color: #fff;
  transition: all 0.3s;
}

.purchase-form .currency-dropdown ul > li > a:hover {
  background: #32373c;
}

.purchase-form .currency-dropdown ul > li > a > .currency-tag {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  line-height: 18px;
  margin-right: 10px;
}

.purchase-form .currency-dropdown ul > li > a > .currency-name {
  color: #bbb;
  font-size: 14px;
  line-height: 14px;
}

.purchase-form .currency-dropdown ul > li > a > img {
  width: 32px;
  height: 32px;
  margin-right: 16px;
}

.purchase-form .currency-dropdown-btn {
  width: 100px;
  position: absolute;
  right: 0;
  top: 10px;
  display: flex;
  align-items: center;
  padding: 6px 10px;
  border-left: none;
}

.purchase-form .currency-dropdown-btn > .currency-info {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.purchase-form .currency-dropdown-btn > .currency-info > .name {
  margin-bottom: 5px;
  color: #bbb;
  font-size: 13px;
  line-height: 12px;
}

.purchase-form .currency-dropdown-btn > .currency-info > .tag {
  color: #fff;
  font-size: 21px;
  font-weight: bold;
  line-height: 13px;
}

.purchase-form .currency-dropdown-btn > i {
  color: #fff;
  margin-left: auto;
  padding-right: 3px;
}

.purchase-form .currency-conversion {
  width: 100px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: absolute;
  right: 0;
  top: 10px;
  padding: 6px 10px;
  border-left: none;
}

.purchase-form .currency-conversion > .name {
  margin-bottom: 5px;
  color: #bbb;
  font-size: 13px;
  line-height: 12px;
}

.purchase-form .currency-conversion > .tag {
  color: #fff;
  font-size: 21px;
  font-weight: bold;
  line-height: 13px;
}

.hero-text {
  position: relative;
  top: -9px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 480px;
  margin-left: 110px;
  color: #fff;
}

.hero-text .hero-title {
  font-size: 52px;
  font-weight: bold;
  line-height: 52px;
  margin-bottom: 30px;
  opacity: 0.99;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.hero-text .hero-paragraph {
  font-size: 17px;
  line-height: 20px;
  color: #bbb;
  opacity: 0.99;
}

.hero-text .crypto-list {
  display: flex;
  margin-top: 20px;
}

.hero-text .crypto-list > li {
  margin-right: 6px;
}

.hero-text .crypto-list > li > img {
  width: 32px;
  height: 32px;
}

@media screen and (max-width: 800px) {
  .hero-text .hero-title {
    display: block;
    text-align: center;
    margin-bottom: 0;
  }

  .hero-text .hero-paragraph {
    display: block;
    text-align: center;
  }

  .hero-text .crypto-list {
    align-items: center;
    justify-content: center;
    margin-bottom: 50px;
  }
}
</style>

<script>
export default {
  layout: 'dark',
  async asyncData({$axios, error}) {
    return await $axios.get('/store/vars').then(response => {
      return {
        storeVars: response.data
      }
    }).catch(exception => {
      console.log('failed to fetch store vars');
      console.log(exception);
      error({statusCode: 500, message: "Failed to connect to the store. Please try again later."})
    });
  },
  data() {
    return {
      storeVars: null,
      error: null,
      updating: false,
      updated: false,
      confirming: false,
      currencies: [
        {
          name: "Bitcoin",
          tag: "BTC",
          icon: require("~/assets/images/bitcoin.png"),
        },
        {
          name: "Ethereum",
          tag: "ETH",
          icon: require("~/assets/images/ethereum.png"),
        },
        {
          name: "Ripple",
          tag: "XRP",
          icon: require("~/assets/images/ripple.png"),
        },
        {
          name: "Cardano",
          tag: "ADA",
          icon: require("~/assets/images/cardano.png")
        },
        {
          name: "Monero",
          tag: "XMR",
          icon: require("~/assets/images/monero.png"),
        },
        {
          name: "Binance",
          tag: "BNB",
          icon: require("~/assets/images/binance.png"),
        },
        {
          name: "Litecoin",
          tag: "LTC",
          icon: require("~/assets/images/litecoin.png"),
        },
        {
          name: "Dogecoin",
          tag: "DOGE",
          icon: require("~/assets/images/doge.png"),
        },
        {
          name: "Tether",
          tag: "USDT",
          icon: require("~/assets/images/tether.png"),
        }
      ],
      currencyName: "Bitcoin",
      currencyTag: "BTC",
      currencyIcon: require("~/assets/images/bitcoin.png"),
      currencyRate: null,
      youSendAmount: 0.00,
      youReceiveAmount: 0.00,
      buyerEmail: "",
    }
  },
  computed: {
    getSupportedCurrenciesNum() {
      return this.currencies.length;
    },
    getNormalizedExchangeRate() {
      return Math.round(((1.0 / this.currencyRate) + Number.EPSILON) * 100) / 100;
    },
    isExtraCreditEnabled() {
      return this.storeVars.extra_credit_enabled;
    },
    getExtraCreditPercentage() {
      return this.storeVars.extra_credit_percentage;
    }
  },
  async mounted() {
    await this.updateExchangeRate();
  },
  methods: {
    async selectCurrency(currency) {
      if (this.confirming) {
        return;
      }

      this.currencyName = currency.name;
      this.currencyTag = currency.tag;
      this.currencyIcon = currency.icon;

      if (this.$refs['currency-dropdown'] !== undefined) {
        window.UIkit.dropdown(this.$refs['currency-dropdown']).hide();
      }

      if (this.youSendAmount > 0) {
        await this.updateExchangeRate().then((exchangeRate) => {
          let receiveAmount = ((this.youSendAmount / exchangeRate) + Number.EPSILON) * 100;

          if (this.storeVars.extra_credit_enabled) {
            receiveAmount = receiveAmount * (1.0 + (this.storeVars.extra_credit_percentage / 100.0));
          }

          this.youReceiveAmount = Math.round(receiveAmount) / 100;
        });
      }
    },
    async startPurchase() {
      this.error = null;
      this.rateUpdated = false;
      this.storeUpdated = false;

      if (isNaN(this.youSendAmount) || this.youSendAmount <= 0.00) {
        this.error = 'You entered an invalid amount!';
        return
      }

      if (this.currencyRate <= 0.00) {
        this.error = 'The exchange rate hasn\'t been updated!';
        return
      }

      const previousRate = this.currencyRate;
      await this.updateExchangeRate().then((exchangeRate) => {
        if (previousRate !== exchangeRate) {
          this.rateUpdated = true;
          return;
        }

        const storeVars = this.storeVars;
        this.updateStoreVars().then(() => {
          if (storeVars.extra_credit_enabled !== this.storeVars.extra_credit_enabled
            || storeVars.extra_credit_percentage !== this.storeVars.extra_credit_percentage) {
            this.storeUpdated = true;
            return
          }

          this.confirming = true;
        });
      });
    },
    confirmPurchase() {
      this.error = null;
      this.rateUpdated = false;
      this.storeUpdated = false;

      if (isNaN(this.youSendAmount) || this.youSendAmount <= 0.00) {
        this.error = 'You entered an invalid amount!';
        return
      }

      if (this.currencyRate <= 0.00) {
        this.error = 'The exchange rate hasn\'t been updated!';
        return
      }

      const previousRate = this.currencyRate;
      this.updateExchangeRate().then((exchangeRate) => {
        if (previousRate !== exchangeRate) {
          this.rateUpdated = true;
          return;
        }

        const storeVars = this.storeVars;
        this.updateStoreVars().then(() => {
          if (storeVars.extra_credit_enabled !== this.storeVars.extra_credit_enabled
            || storeVars.extra_credit_percentage !== this.storeVars.extra_credit_percentage) {
            console.log('store updated');
            this.storeUpdated = true;
            return
          }

          this.updating = true;

          const postData = {
            'currency': this.currencyTag,
            'amount': this.youSendAmount,
            'exchange_rate': this.currencyRate,
            'buyer_email': this.buyerEmail,
          };

          if (this.storeVars.extra_credit_enabled) {
            postData.extra_credit_percentage = this.storeVars.extra_credit_percentage;
          }

          this.$axios.post('/store/tx/create', postData).then(response => {
            if (response.status === 200) {
              this.$store.commit('addTransaction', response.data);
              this.$store.commit('saveTransactionHistory');
              this.$router.push({name: 'transaction-id', params: {'id': response.data.id}})
            } else {
              throw 'Unexpected response status';
            }
          })
            .catch(error => {
              if (error.response) {
                if (error.response.data === 'EXCHANGE_RATE_MISMATCH') {
                  this.rateUpdated = true;
                  return
                }

                if (error.response.data === 'EXTRA_CREDIT_INVALID') {
                  this.storeUpdated = true;
                  return;
                }

                this.error = error.response.data;
              }

              this.updating = false;
            });
        });
      });
    },
    async onUpdateReceiveAmount() {
      return await this.updateExchangeRate().then((exchangeRate) => {
        this.youSendAmount = this.round(this.youReceiveAmount / exchangeRate, 6);
      });
    },
    async onUpdateSendAmount() {
      return await this.updateExchangeRate().then((exchangeRate) => {
        this.youReceiveAmount = this.round(this.youSendAmount * exchangeRate, 2);

        if (this.storeVars.extra_credit_enabled) {
          this.youReceiveAmount = this.round(this.youReceiveAmount * (1.0 + (this.storeVars.extra_credit_percentage / 100.0)), 2);
        }
      });
    },
    async updateStoreVars() {
      return await this.$axios.get('/store/vars').then(response => {
        this.storeVars = response.data;
        return this.storeVars;
      });
    },
    async updateExchangeRate() {
      this.updating = true;

      return await this.$axios.get('/store/exchange-rate?currency=' + this.currencyTag).then(response => {
        if (response.status === 200) {
          this.currencyRate = response.data.rate;
        }

        this.updating = false;

        return this.currencyRate;
      })
        .catch(error => {
          console.log(error);
          this.error = 'Failed to update exchange rate';
          this.updating = false;
        });
    },
    round(value, decimals) {
      return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
    },
    goBack() {
      this.error = null;
      this.updated = false;
      this.confirming = false;
    },
    getCurrencyIcon(tag) {
      for (const i in this.currencies) {
        const currency = this.currencies[i];
        if (currency.tag === tag) {
          return currency.icon;
        }
      }
      return null;
    }
  },
  head() {
    return {
      title: 'Pay Using Crypto'
    }
  }
}
</script>
