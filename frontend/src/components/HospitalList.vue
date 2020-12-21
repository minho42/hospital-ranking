<template>
  <div class="flex flex-col items-center">
    <div>
      <div class="bg-gray-200 rounded-md p-2">
        <label v-for="(state, index) in states" :key="index" class="inline-flex items-center">
          <input type="checkbox" :value="state" class="form-checkbox w-4 h-4 align-middle" v-model="checkedStates" />
          <span class="ml-1 mr-5">{{state}}</span>  
        </label>
      </div>
    </div>
    <div>
      <div class="bg-gray-200 rounded-md p-2 my-2">
        <label v-for="(sector, index) in sectors" :key="index" class="inline-flex items-center">
          <input type="radio" :value="sector"  class="form-radio w-4 h-4 align-middle" v-model="selectedSector" />
          <span class="ml-1 mr-5">{{sector}}</span>
        </label>

      </div>
    </div>
    
    <div v-if="isLoading" class="text-xl font-bold py-3">
      Loading...
    </div>
        
    <div v-else class="text-2xl font-bold py-3">
      {{ filteredRankingData.length }} hospitals
      <span v-show="getAverateStar">({{ getAverateStar.toFixed(2) }})</span>
    </div>
    <div>
      <ul>
        <li>
          <Hospital
            v-for="(data, index) in filteredRankingData"
            :key="data.name"
            :index="index + 1"
            :sector="data.sector"
            :state="data.state"
            :name="data.name"
            :stars="data.stars"
            :reviews="data.reviews"
          />
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Hospital from "./Hospital.vue";

export default {
  name: "HospitalList",
  data() {
    return {
      states:["VIC", "NSW", "QLD", "TAS", "WA", "SA", "ACT", "NT"],
      checkedStates: ["VIC", "NSW", "QLD", "TAS", "WA", "SA", "ACT", "NT"],
      sectors: ["ALL", "PUBLIC", "PRIVATE"], 
      selectedSector: "ALL",
    };
  },
  components: {
    Hospital,
  },
  props: {
    rankingData: Array,
    isLoading: Boolean,
  },
  methods: {},
  computed: {
    getAverateStar: function () {
      return this.getStarsXreviews / this.getTotalReviewCount;
    },
    getStarsXreviews: function () {
      let total = 0;
      [...this.filteredRankingData].map((item) => {
        total += parseFloat(item.stars) * parseFloat(item.reviews);
      });
      return parseInt(total);
    },
    getTotalReviewCount: function () {
      let total = 0;
      [...this.filteredRankingData].map((item) => {
        total += parseInt(item.reviews);
      });
      return total;
    },
    sortedRankingData: function () {
      return [...this.rankingData].sort((a, b) => {
        return parseFloat(b.ranking) - parseFloat(a.ranking);
      });
    },
    filteredRankingData: function () {
      return this.sortedRankingData
      .filter((item) => {
        return this.checkedStates.includes(item.state);
      })
      .filter((item)=>{
        if (this.selectedSector === "ALL") {
          return true
        }
        return this.selectedSector===item.sector
      })
    },
  },
};
</script>

<style scoped>
</style>
