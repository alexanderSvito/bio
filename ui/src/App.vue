<template>
  <div>
    <Header />
    <div class="content">
      <router-view/>
    </div>
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    Header
  },
  data: () => ({
    //
  }),
};
</script>

<style scoped>
.content {
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
</style>
