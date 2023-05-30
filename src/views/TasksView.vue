<template>
    <!-- make this button work -->
    <button @click="incr">count is: {{ count }}</button>
    <input type="range" min="0" max="10" v-model="count" />
</template>

<script lang="ts">
export default {
    data() {
        return {
            count: 0,
        };
    },
    methods: {
        incr() {
            this.count++;
        },
    },
};
</script>
