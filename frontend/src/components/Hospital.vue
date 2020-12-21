<template>
  <div class="flex items-center justify-center">
    <div
      class="w-full px-3 pt-1 pb-2 bg-white rounded-md border-b border-gray-400"
    >
      <div class="flex items-start text-gray-800">
        <div class="font-semibold text-gray-600">
          {{ index }}.
        </div>
        <div class="flex-1 flex-col pl-2">
          <div class="inline-flex font-medium ">
            {{ name }}
          </div>
          <div class="flex items-center justify-start">
            <div class="inline-flex font-medium bg-green-200 rounded-lg px-1">
              {{ stars }}
            </div>
            <div class="flex-1 pl-1">({{ reviews }})</div>
            <div class="text-sm">
              {{ state }}
            </div>
            <div
              class="text-sm ml-3 rounded-md px-1"
              :class="sector === 'PUBLIC' ? 'bg-indigo-200' : 'bg-pink-200'"
            >
              {{ sector }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Hospital",
  props: {
    index: Number,
    sector: String,
    state: String,
    name: String,
    stars: String,
    reviews: String,
  },
};
</script>

<style scoped></style>
