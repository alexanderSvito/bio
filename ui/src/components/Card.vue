<template>
  <div :class="[{'loading': loading}, 'card']">
    <v-progress-linear
      v-if="loading"
      indeterminate
      style="margin-top: -2px;"
      color="primary"
    ></v-progress-linear>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped lang="scss">
  .card {
    background: white;
    margin: 30px;

    border-top: black 2px solid;

    font-size: 16px;
    font-family: 'Lato';

    &.loading {
      border-top: 0;
    }
  }
</style>
