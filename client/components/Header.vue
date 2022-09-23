<template>
  <header class="catalin-header">
    <div class="header-hover" id="header-hover"></div>
    <div class="catalin-header-content">
      <div class="uk-container">
        <div class="coloana-3" id="coloana-3">
          <div class="cutie-1" id="cutie-1" data-toggle="tooltip" data-placement="top" title="" data-original-title="Click to join">
            <ul class="no-padding-margin">
              <a href="https://discord.gg/KQDb4c55fE" id="discord_invite_link" target="_blank" style="text-decoration: none;">
                <ul class="directia-elementelor-secundare no-padding-margin">
                  <li class="element-secundar">
                    <h3>Discord Server</h3>
                  </li>
                  <li class="element-secundar">
                    <p><span id="discord-count">{{ $store.getters['getDiscordMemberCount'] }}</span> Online now</p>
                  </li>
                </ul>
                <ul class="directie-elemente no-padding-margin">
                  <li class="principalul-element"><i class="fab fa-discord discord-spatiu"></i></li>
                </ul>
              </a>
            </ul>
          </div>
          <div class="cutie-2" id="cutie-2">
            <a href="/">
              <img src="~assets/images/hcrivals.png" id="logo" class="logo-counter img-responsive">
            </a>
          </div>
          <div class="cutie-3" id="cutie-3" data-toggle="tooltip" data-placement="top" title="" data-original-title="Copy the ip">
            <a style="text-decoration: none;" id="copiazaIP" v-on:click="copyServerAddress" uk-tooltip="title: Click to copy the server IP!">
              <ul class="directie-elemente no-padding-margin">
                <li class="principalul-element"><i class="fas fa-play-circle server-spatiu"></i></li>
              </ul>
              <ul class="directia-elementelor-secundare" style="margin-right: 0px; padding: 0; margin-bottom: 0px;">
                <li class="element-secundar">
                  <h3 class="play-button-design"><span class="player-count">{{ $store.getters['getPlayerCount'] }}</span> Players online</h3>
                </li>
                <li class="element-secundar">
                  <p class="play-button-design-gray">Start adventure</p>
                </li>
              </ul>

              <p class="copy-popup uk-p uk-p-green uk-animation-fade" ref="copy-popup" v-show="copied">Server address copied to clipboard!</p>
            </a>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
#logo {
  display: block;
  width: 200px;
  margin: 0 auto;
}

.steluta {
  position: absolute;
  top: -7px;
  right: 0;
  left: 0;
  transition: all .15s;
}

.catalin-header {
  background-size: cover;
  position: relative;
  z-index: 1020;
  background: #be2727 no-repeat;
  overflow: hidden;
}

.catalin-header .catalin-header-content {
  text-align: center;
  top: 50%;
  margin-top: 80px;
  padding-bottom: 80px;
  background: linear-gradient(transparent 0, rgba(0, 0, 0, .18) 30%, #262b2f 100%);
  position: relative;
  z-index: 999;
}

.header-hover {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background-size: cover !important;
  background-repeat: no-repeat !important;
  z-index: 2;
  background: url('https://i.imgur.com/yNNjYat.png');
  background-position: center;
  opacity: 0.29;
  filter: blur(2px);
}

.catalin-header .catalin-navigatie {
  padding: 20px 0;
  background: rgba(255, 255, 255, .05);
  box-shadow: 0 3px 6px rgb(0 0 0 / 8%), 0 3px 6px rgb(0 0 0 / 2%);
  position: relative;
  z-index: 1020;
}

.catalin-header .catalin-nav-links {
  display: flex;
  align-items: center;
  justify-content: center;
}

.catalin-header .catalin-nav-links li {
  display: inline-block;
}

#testare-hide {
  display: inline-block;
}

.catalin-header .catalin-nav-links li {
  display: inline-block;
}

.catalin-header .catalin-nav-links li a:not(:nth-child(2)) {
  margin-left: 10px;
}

.catalin-header .catalin-nav-links li .store {
  background: var(--principal-color);
  position: relative;
  padding: 15px 35px;
  text-align: center;
  font-weight: 700;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  border-bottom: 2px solid rgba(0, 0, 0, .2);
  border-radius: 50px;
}

.catalin-header .catalin-nav-links li a {
  display: inline-block;
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  transition: all .3s;
  text-shadow: 4px 4px 2px rgba(0, 0, 0, 0.08);
  padding: 15px 15px;
  border-bottom: 1px solid transparent;
  position: relative;
}

.catalin-header .catalin-nav-links li a:not(:nth-child(2)) {
  margin-left: 10px;
}

.catalin-header .catalin-nav-links li .store {
  background: #be2727;
  position: relative;
  padding: 15px 35px;
  text-align: center;
  font-weight: 700;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  border-bottom: 2px solid rgba(0, 0, 0, .2);
  border-radius: 50px;
}

.coloana-3 {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.coloana-3 .cutie-1 {
  flex: 1;
  text-align: center;
}

.coloana-3 .cutie-2 {
  flex: 1;
}

.coloana-3 .cutie-3 {
  flex: 1;
  text-align: center;
}

.no-padding-margin {
  margin: 0 !important;
  padding: 0 !important;
}

a {
  color: #be2727;
  text-decoration: none;
}

#logo-server {
  width: 250px !important;
  transform: scale(1.5);
}

.directia-elementelor-secundare {
  display: inline-block;
  vertical-align: middle;
  margin-left: 15px !important;
  list-style: none;
}

.directie-elemente {
  display: inline-block;
  vertical-align: middle;
  list-style: none;
  padding: 0;
  margin: 0;
}

.directia-elementelor-secundare .element-secundar h3 {
  color: #be2727;
  font-weight: 700;
  font-size: 1.17em;
  margin: 0;
  text-align: left;
}

.coloana-3 .cutie-1 p {
  text-align: right;
}

.directia-elementelor-secundare .element-secundar p {
  color: #fff;
  margin: 0;
  text-align: left;
}

.directie-elemente .principalul-element .discord-spatiu {
  margin-left: 10px;
}

.directie-elemente .principalul-element i {
  background: #00000014;
  padding: 15px;
  border-radius: 5px;
  font-size: 35px;
  color: #be2727;
}

#copiazaIP {
  position: relative;
}

.copy-popup {
  position: absolute;
}
</style>

<script>
export default {
  data() {
    return {
      copied: false
    }
  },
  methods: {
    copyServerAddress(event) {
      event.preventDefault();

      this.$clipboard('play.hcrivals.org'); // copy to clipboard

      let ins = this;
      ins.copied = true;

      setTimeout(function () {
        ins.copied = false;
      }, 3000);
    }
  },
  mounted() {

  }
}
</script>
