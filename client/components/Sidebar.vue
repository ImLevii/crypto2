<template>
    <div class="page-section">
        <div class="sidebar">
            <div class="slot" v-for="index in slots" :key="index">
                <slot :name="'slot-' + index">Empty slot {{ index }}</slot>
            </div>
        </div>
    </div>
</template>

<style scoped>
.page-section {
	padding: 20px;
}

.sidebar .slot {
    position: relative;
    margin-bottom: 20px;
}

.sidebar .slot:last-child {
    margin-bottom: 0;
}

.sidebar .slot > .body {
    margin-top: 1px;
}
</style>

<script>
export default {
    props: {
        slots: {
            type: Number,
            required: true
        }
    }
}
</script>
