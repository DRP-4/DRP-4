<script lang="ts">
import Satisifed from "@/components/icons/Satisfied.vue";
import Neutral from "@/components/icons/Neutral.vue";
import Dissatisfied from "@/components/icons/Dissatisfied.vue";

export default {
    props: {
        name: {
            type: String,
            required: true,
        }
    },
    components: {
        Satisifed,
        Neutral,
        Dissatisfied,
    },
    emits: ["satisfied", "neutral", "dissatisfied"],
}
</script>

<template>
    <div class="centered">
        <div class="form-horizontal border p-3 rounded thecard">

            <div class="centered">
                <h2> How was session {{ name }}?</h2>
            </div>


            <div class="centered">
                <div class="emotions">
                    <div @click="$emit('satisfied')" class="face">
                        <Satisifed />
                    </div>
                    <div @click="$emit('neutral')" class="face">
                        <Neutral />
                    </div>
                    <div @click="$emit('dissatisfied')" class="face">
                        <Dissatisfied />
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<style scoped>
.centered {
    display: flex;
    align-items: center;
    justify-content: center;
}

.thecard {
    display: grid;
}

.emotions {
    display: flex;
    gap: 2em;
    margin: 1em;
}


.face {
    transition: transform .2s;
}


.face:hover {
    transform: scale(1.2);
}
</style>