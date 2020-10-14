<template>
  <v-app>
    <Header/>
    <div class="content">
      <transition :name="transitionName"
                mode="out-in"
              @beforeLeave="beforeLeave"
              @enter="enter"
              @afterEnter="afterEnter">

        <router-view/>
      </transition>
    </div>
    <footer>
    Copyright
    </footer>
  </v-app>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    Header
  },
  created() {
    this.$router.beforeEach((to, from, next) => {
      const toDepth = to.path.split('/').filter(item => item).length;
      const fromDepth = from.path.split('/').filter(item => item).length;
      let transitionName = toDepth < fromDepth ? 'slide-right' : 'slide-left';

      this.transitionName = transitionName;

      next();
    });
  },
  data: () => ({
    prevHeight: 0,
    transitionName: 'slide-left'
  }),
  methods: {
      beforeLeave(element) {
        this.prevHeight = getComputedStyle(element).height;
      },
      enter(element) {
        const { height } = getComputedStyle(element);

        element.style.height = this.prevHeight;

        setTimeout(() => {
          element.style.height = height;
        });
      },
      afterEnter(element) {
        element.style.height = 'auto';
      },
    },
};
</script>

<style>
button {
  border-radius: 0 !important;
}
body {
  margin: none;
}
.content {
  display: flex;
  width: 100%;
  justify-content: flex-start;
  align-items: center;
  flex-direction: column;

  font-family: 'Lato';

  min-height: 95vh;
  background: #fafafa;
}

.v-application#app {
  background: #fafafa;
}

slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition-duration: 0.3s;
  transition-property: height, opacity, transform;
  transition-timing-function: ease-in-out;
  overflow: hidden;
}

.slide-left-enter,
.slide-right-leave-active {
  opacity: 0;
  transform: translate(5em, 0);
}

.slide-left-leave-active,
.slide-right-enter {
  opacity: 0;
  transform: translate(-5em, 0);
}
</style>
