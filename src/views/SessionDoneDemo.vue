<template>
    <div class="wrap">
        <PostSessionFeedback name="1" @satisfied="console.log('green')" @neutral="console.log('neutral')"
            @dissatisfied="console.log('bad')" />
    </div>
</template>

<script lang="ts">
import PostSessionFeedback from "@/components/PostSessionFeedback.vue";

export default {
    components: { PostSessionFeedback },
};
</script>

<style scoped>
.wrap {
    margin-top: 100px;
}
</style>