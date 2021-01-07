<template>
  <div id="app">
    <Navbar />
    <HospitalList :rankingData="rankingData" :isLoading="isLoading" />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import HospitalList from "./components/HospitalList.vue";
import rankingData from '../ranking.json'

export default {
  name: "App",
  components: {
    Navbar,
    HospitalList,
  },
  data() {
    return {
      rankingData,
      isLoading: true,
      isErrored: false,
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
ul {
  list-style-type: none;
}
</style>
