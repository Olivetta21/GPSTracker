<template>
    <div class="loading-icon">
        <div></div>
    </div>
</template>

<style scoped>
.loading-icon {
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.loading-icon>div {
    border: 4px solid rgba(155, 155, 155, 0.5);
    border-top: 4px solid white;
    border-bottom: 4px solid black;
    border-radius: 50%;
    height: 100%;
    width: 100%;
    max-width: 50px;
    max-height: 50px;
    aspect-ratio: 1;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
</style>