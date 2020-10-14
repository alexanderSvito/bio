<template>
  <header>
    <div class="logo">
      <router-link :to="{ name: 'Main', params: {} }">
        <img src="../assets/logo.svg" height="50">
      </router-link>
    </div>
    <router-link :to="{ name: 'Register', params: {} }">Register</router-link>

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

<style scoped lang='scss'>
header {
  display: flex;
  align-items: center;
  justify-content: space-around;
  position: relative;

  border-bottom: 2px solid black;

  background: white;
  height: 90px;

  color: black;
  font-size: 16px;
  font-family: 'Roboto';
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

.logo img:hover {
  cursor: pointer;
  fill: #0330fc;
}

header a {
  font-family: 'Roboto';
  text-decoration: none;
  color: black;
  font-size: 24px;
  transition: all 0.1s ease-in-out;
  position: relative;

  &:before,
  &:after {
    content: "";
    position: absolute;
    bottom: -10px;
    width: 0px;
    transition: all 0.1s ease-in-out;
    height: 5px;
    margin: 5px 0 0;
    opacity: 0;
    background-color: #0330fc;
  }

  &:before {
    left: 50%;
  }
  &:after {
    right: 50%;
  }
}

a:hover {
  color: #0330fc;
  &:before,
  &:after {
    width: 52%;
    opacity: 1;
  }
}

</style>
