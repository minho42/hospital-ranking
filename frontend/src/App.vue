<template>
  <div id="app">
    <Navbar />
    <HospitalList :rankingData="rankingData" />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import HospitalList from "./components/HospitalList.vue";
import rankingData from "../ranking.json";

export default {
  name: "App",
  components: {
    Navbar,
    HospitalList,
  },
  data() {
    return {
      rankingData,
      isErrored: false,
    };
  },
};
</script>
