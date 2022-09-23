export default {
    /*
     ** Nuxt rendering mode
     ** See https://nuxtjs.org/api/configuration-mode
     */
    ssr: false,
    /*
     ** Nuxt target
     ** See https://nuxtjs.org/api/configuration-target
     */
    target: 'static',
    /*
     ** Headers of the page
     ** See https://nuxtjs.org/api/configuration-head
     */
    head: {
        titleTemplate: 'HCRivals | %s',
        meta: [
            {
                charset: 'utf-8'
            },
            {
                name: 'viewport', content: 'width=device-width, initial-scale=1, viewport-fit=cover'
            },
            {
                hid: 'description',
                name: 'description',
                content: 'The official crypto payment gateway for HCRivals!',
            },
            {
                name: 'referrer',
                content: 'no-referrer'
            }
        ],
        script: [
            {
                src: 'https://cdn.jsdelivr.net/npm/uikit@3.5.7/dist/js/uikit.min.js'
            },
            {
                src: 'https://cdn.jsdelivr.net/npm/uikit@3.5.7/dist/js/uikit-icons.min.js'
            },
            {
                src: 'https://kit.fontawesome.com/1250b98b47.js'
            },
            {
                src: 'https://www.google.com/recaptcha/api.js?onload=vueRecaptchaApiLoaded&render=explicit'
            },
        ],
        link: [
            {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'},
            {rel: 'icon', type: 'image/x-icon', href: '/apple-touch-icon.png', sizes: '180x180'},
            {rel: 'icon', type: 'image/x-icon', href: '/favicon-32x32.png', sizes: '32x32'},
            {rel: 'icon', type: 'image/x-icon', href: '/favicon-16x16.png', sizes: '16x16'},
            {rel: 'manifest', 'href': '/site.webmanifest'},
            {
                rel: 'stylesheet',
                type: 'text/css',
                href: 'https://cdn.jsdelivr.net/npm/uikit@3.5.7/dist/css/uikit.min.css'
            },
        ],
    },
    /*
     ** Global CSS
     */
    css: [
        {
            src: '~assets/styles/client.css'
        }
    ],
    /*
     ** Plugins to load before mounting the App
     ** https://nuxtjs.org/guide/plugins
     */
    plugins: [
        '~/plugins/client',
        '~/plugins/clipboard',
        '~/plugins/inject',
        '~/plugins/timeago',
        '~/plugins/vuelidate',
    ],
    /*
     ** Auto import components
     ** See https://nuxtjs.org/api/configuration-components
     */
    components: true,
    /*
     ** Nuxt.js dev-modules
     */
    buildModules: [
        // Doc: https://github.com/nuxt-community/eslint-module
        // '@nuxtjs/eslint-module',
    ],
    /*
     ** Nuxt.js modules
     */
    modules: [
        // Doc: https://axios.nuxtjs.org/usage
        '@nuxtjs/axios',
        '@nuxtjs/auth-next',
        '@nuxtjs/markdownit',
    ],
    // [optional] markdownit options
    // See https://github.com/markdown-it/markdown-it
    markdownit: {
        xhtmlOut: false,
        linkify: true,
        breaks: false,
        use: [
            'markdown-it-div',
            'markdown-it-imsize',
            // 'markdown-it-attrs'
        ],
        injected: true
    },
    /*
       ** Axios module configuration
       ** See https://axios.nuxtjs.org/options
       */
    axios: {
        baseURL: 'http://127.0.0.1:8000/api',
        progress: true
        // https: true TODO: needs to be enabled for production
    },
    /*
   ** Build configuration
   ** See https://nuxtjs.org/api/configuration-build/
   */
    build: {
        /*
         ** You can extend webpack config here
         */
        extend(config, ctx) {
            config.node = {
                fs: 'empty'
            };
            config.devServer = {
                clientLogLevel: "silent",
            };

        },
        hotMiddleware: {
            client: {
                overlay: false
            }
        }
    }
}
