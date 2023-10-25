<template>
  <div>
    <div class="trucks backdrop"></div>
    <HeaderComponent />
    <div class="main">
      <div
        class="bubble"
        @mouseover="showTooltip = true"
        @mouseleave="showTooltip = false"
      >
        <i class="fas fa-plus"></i>
      </div>
      <div v-if="showTooltip" class="tooltip">Add New Truck Entry</div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th v-for="(column, index) in visibleColumns" :key="index">
                <div class="header-content">
                  <transition name="fade" mode="out-in">
                    <div
                      class="label-sort"
                      v-if="index !== activeSearchColumnIndex"
                      key="label-sort"
                    >
                      <div
                        class="label"
                        v-show="column.sortable"
                        @click="activateSearch(index)"
                      >
                        {{ column.label }}
                      </div>
                      <div
                        class="sort"
                        v-show="column.sortable"
                        @click="toggleSort(column)"
                      >
                        <span
                          class="up-arrow"
                          :class="{ active: column.sortDirection === 'asc' }"
                          >▲</span
                        >
                        <span
                          class="down-arrow"
                          :class="{ active: column.sortDirection === 'desc' }"
                          >▼</span
                        >
                      </div>
                    </div>
                    <input
                      v-else
                      class="search"
                      v-model="column.search"
                      @input="filterData"
                      key="search-input"
                      :ref="'searchInput-' + index"
                    />
                  </transition>
                </div>
              </th>
            </tr>
          </thead>
          <tbody ref="tbodyElement">
            <tr v-for="truck in filteredTrucks" :key="truck.id">
              <td v-for="(column, colIndex) in visibleColumns" :key="colIndex">
                <router-link
                  :to="{
                    name: 'truck-details',
                    params: { id: findTruckIdByVin(truck.vin) },
                  }"
                  class="truck-link"
                >
                  <template
                    v-if="column.field !== 'color' && column.field !== 'user'"
                  >
                    {{ truck[column.field] }}
                  </template>
                  <template
                    v-if="column.field === 'color' && column.field !== 'user'"
                  >
                    <div
                      class="color-square"
                      :style="{ backgroundColor: truck.color }"
                    ></div>
                  </template>
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import HeaderComponent from "../components/HeaderComponent.vue";

export default {
  data() {
    return {
      columns: [],
      trucks: [],
      filteredTrucks: [],
      activeSearchColumnIndex: null,
      showTooltip: false,
    };
  },
  computed: {
    filteredData() {
      return this.trucks;
    },
    visibleColumns() {
      return this.columns.slice(2);
    },
  },
  mounted() {
    this.fetchData();
  },
  name: "TrucksView",
  components: {
    HeaderComponent,
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(
          "https://maris.com:8020/api/truck/trucks/",
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        );

        if (response.data.length > 0) {
          const firstTruck = response.data[0];
          this.columns = Object.keys(firstTruck).map((key) => ({
            label: key.replace(/_/g, " ").toUpperCase(),
            field: key,
            sortable: true,
            search: "",
            sortDirection: "asc",
          }));
        }

        this.trucks = response.data;
        this.filteredTrucks = [...this.trucks];
        this.sortData();
      } catch (error) {
        console.error(error);
      }
    },
    toggleSort(column) {
      column.sortDirection = column.sortDirection === "asc" ? "desc" : "asc";
      this.sortData(column);
      this.filteredTrucks = [...this.trucks];
    },
    sortData(sortableColumn) {
      sortableColumn =
        sortableColumn || this.columns.find((column) => column.sortDirection);
      if (!sortableColumn) return;

      this.trucks.sort((a, b) => {
        const field = sortableColumn.field;
        const valA = a[field];
        const valB = b[field];

        if (!isNaN(valA) && !isNaN(valB)) {
          const sortResult =
            sortableColumn.sortDirection === "asc" ? valA - valB : valB - valA;
          return sortResult;
        }

        // Handle null or undefined values
        if (!valA) return sortableColumn.sortDirection === "asc" ? 1 : -1;
        if (!valB) return sortableColumn.sortDirection === "asc" ? -1 : 1;

        const regex = /[^a-zA-Z0-9]/g;
        const strA = valA.replace(regex, "").toUpperCase();
        const strB = valB.replace(regex, "").toUpperCase();

        const stringSortResult =
          sortableColumn.sortDirection === "asc"
            ? strA.localeCompare(strB)
            : strB.localeCompare(strA);
        return stringSortResult;
      });
      this.filteredTrucks = [...this.trucks];
    },
    activateSearch(index) {
      if (this.activeSearchColumnIndex !== null) {
        this.deactivateSearch();
      }
      this.activeSearchColumnIndex = index;
      this.$nextTick(() => {
        setTimeout(() => {
          this.$el.querySelector(".search").focus();
          // Add a click event listener to the document
          document.addEventListener("click", this.handleDocumentClick);
        }, 550);
      });
    },
    clearSearchInput() {
      this.visibleColumns.forEach((column) => {
        column.search = "";
      });
    },
    deactivateSearch() {
      this.activeSearchColumnIndex = null;
      this.filteredTrucks = [...this.trucks];
      this.visibleColumns.forEach((column) => {
        column.search = "";
      });
      // Remove the click event listener from the document
      document.removeEventListener("click", this.handleDocumentClick);
    },
    filterData() {
      const searchColumn = this.visibleColumns[this.activeSearchColumnIndex];
      const searchTerm = searchColumn.search.toLowerCase();
      this.filteredTrucks = this.trucks.filter((truck) =>
        String(truck[searchColumn.field]).toLowerCase().startsWith(searchTerm)
      );
    },
    findTruckIdByVin(vin) {
      const truck = this.trucks.find((truck) => truck.vin === vin);
      return truck ? truck.id : null;
    },
    handleDocumentClick(event) {
      // Check if the click event target is outside both the input and the table body
      const isOutsideInput =
        event.target !== this.$el.querySelector(".search") &&
        !event.target.closest(".search"); // Check for input and its descendants
      const isOutsideTableBody =
        event.target !== this.$refs.tbodyElement &&
        !event.target.closest(".table-container tbody"); // Check for tbody and its descendants

      if (isOutsideInput && isOutsideTableBody) {
        // Deactivate the search when clicking outside
        this.deactivateSearch();
      }
    },
  },
  watch: {
    activeSearchColumnIndex: {
      handler(newValue) {
        if (newValue !== null) {
          this.$nextTick(() => {
            setTimeout(() => {
              const refArray = this.$refs["searchInput-" + newValue];
              if (refArray && refArray[0]) {
                refArray[0].focus();
              } else {
                console.warn("Reference to search input not found");
              }
            }, 550);
          });
        }
      },
      immediate: false,
    },
  },
};
</script>

<style scoped>
.label-sort {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  flex-grow: 1;
}

.sort {
  display: flex;
  flex-direction: column;
  align-items: center;
}

td,
th {
  min-width: 130px;
  padding: 5px 5px;
}
.fade-enter-active {
  transition: opacity 0.2s ease-in 0.2s; /* ease-in and delay */
}
.fade-leave-active {
  transition: opacity 0.2s ease-out;
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
input {
  width: 120px;
}
</style>
