import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import ru from 'vuetify/es5/locale/ru'
import 'vuetify/dist/vuetify.min.css'



Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#000000',
        secondary: '#4A00E0',
        accent: '#8E2DE2',
        error: '#b71c1c',
      },
    },
  },
  lang: ru
});
