<template>
  <header>
    <div class="logo">
      <img src="../assets/bee.svg" height="50" width="50">
      <span>Биология Тесты</span>
    </div>
    <router-link :to="{ name: 'Register', params: {} }">Зарегистрироваться</router-link>

  </header>
</template>

<script>
import { mapGetters } from 'vuex'


export default {
  name: 'Header',
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'getUser'
    ])
  }
}
</script>

<style scoped>
header {
  display: flex;
  align-items: center;
  justify-content: space-around;
  position: relative;

  background: linear-gradient(45deg, #00b09b, #96c93d);
  height: 90px;
  box-shadow: grey 0px 1px 5px;


  color: white;
  font-size: 16px;
  font-family: 'Pacifico', cursive;
  padding: 1em;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: space-around;
  font-size: 24px;

  position: absolute;
  left: 40px;
  top: 20px;
}

.logo:hover {
  cursor: pointer;
}

a {
  font-family: 'Merriweather Sans', sans-serif;
  text-decoration: none;
  color: white;
}
</style>
