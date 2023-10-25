<template>
  <LoginDialog />
</template>

<script>
import LoginDialog from "../components/LoginDialog.vue";
export default {
  components: {
    LoginDialog,
  },
};
</script>

<style>
.login {
  width: 50%;
  padding: 20px;
  margin: 10% auto;
  background: white;
  opacity: 0.6;
  border-radius: 12px;
}
</style>
