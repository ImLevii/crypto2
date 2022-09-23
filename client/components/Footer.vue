<template>
  <div class="footer-premium">
    <div class="footer-copyright">
      <div class="uk-container">
        <div class="footer-copyright-flex">
          <div class="branding">
            © 2021 HCRivals All Rights Reserved.
          </div>

          <ul>
            <li><a href="https://twitter.com/hcrivals"><i class="fab fa-twitter"></i></a></li>
            <li><a href="https://youtube.com/hcrivals"><i class="fab fa-youtube"></i></a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.footer-premium {
  background: #2c3136;
  color: #888;
  margin-top: 60px;
}

.footer-premium-flex {
  display: flex;
  flex-direction: row;
}

.col-footer {
  margin-right: 30px;
  flex: 1;
  padding: 25px 0;
  line-height: 24px;
}

.col-footer h3 {
  margin: 0;
  margin-bottom: 20px;
  color: #fff;
  font-size: 19px;
  font-weight: 700;
}

.col-footer p {
  margin-bottom: 20px;
}

.col-footer ul {
  list-style-type: none !important;
  padding: 0;
  margin-bottom: 0;
}

.col-footer ul li a {
  display: block;
  padding-bottom: 10px;
  margin-bottom: 10px;
  font-size: 14px;
  text-decoration: none;
  color: #888;
  border-bottom: 1px dotted #404040;
  transition: all .3s;
}

.footer-copyright {
  background: rgba(0, 0, 0, .2);
  border-bottom: 1px solid #2c3136;
}

.footer-copyright-flex {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0;
}

.footer-copyright p {
  padding: 10px 0;
  margin: 0;
  padding: 0;
}

.copyright-footer {
  font-weight: 600;
  color: #888;
  text-decoration: none;
  display: block;
  transition: all .3s;
}

.footer-copyright ul {
  list-style-type: none;
  padding: 0;
  margin-bottom: 0;
}

.footer-copyright ul li {
  display: inline-block;
  margin: 5px;
}

.footer-copyright ul li a {
  background: rgba(0, 0, 0, .05);
  color: #fff;
  font-size: 17px;
  display: block;
  border-bottom: 3px solid rgba(0, 0, 0, .05);
  width: 36px;
  height: 36px;
  line-height: 36px;
  text-align: center;
}

.col-footer .footer-store {
  padding: 12px 30px;
  font-family: Montserrat, sans-serif;
  font-weight: 600;
  background: #FCB602;
  font-size: 13px;
  border-radius: 2px;
  color: #fff;
  text-decoration: none;
  text-shadow: 0 2px 2px rgb(0 0 0 / 10%);
}
</style>

<script>
export default {
  data() {
    return {}
  }
}
</script>
