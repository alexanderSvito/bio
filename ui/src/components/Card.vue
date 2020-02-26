<template>
  <div class="card">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'Card',
}
</script>

<style scoped>
  .card {
    background: white;
    margin: 30px;
    border-radius: 10px;

    line-height: 1.5em;

    border: rgb(232, 240, 254) 1px solid;
    box-shadow: gray 3px 3px 5px;

    font-size: 28px;
    font-family: 'Alegreya', serif;
  }
</style>
