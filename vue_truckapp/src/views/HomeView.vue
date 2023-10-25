<template>
  <div>
    <div class="home backdrop">
      <HeaderComponent />
      <div class="main">
        <img alt="Vue logo" src="../assets/static_images/logo.png" />
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from "../components/HeaderComponent.vue";
export default {
  name: "HomeView",
  components: {
    HeaderComponent,
  },
  data() {
    return {};
  },
  methods: {},
};
</script>
