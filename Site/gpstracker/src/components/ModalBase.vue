<template>
    <div class="modal-base-container" @click.self="$emit('close')">
        <div class="modal-base-content">
            <slot></slot>
        </div>
    </div>
</template>


<script>
    export default {
        emits: ["close"]
    };
</script>


<style scoped>

.modal-base-container {
    position: absolute;
    z-index: 1;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.modal-base-content {
    background-color: white;
    padding: 10px;
    border-radius: 5px;
}

</style>