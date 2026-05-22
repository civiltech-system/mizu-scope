<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <NuxtLink to="/" class="flex items-center space-x-2">
            <span class="text-2xl font-bold text-blue-600">MizuMap</span>
            <span class="text-sm text-gray-400 hidden sm:inline">水質マップ</span>
          </NuxtLink>
          <nav class="flex items-center space-x-6 text-sm font-medium text-gray-600">
            <NuxtLink to="/" class="hover:text-blue-600 transition-colors">地図</NuxtLink>
            <NuxtLink to="/bottled-water" class="hover:text-blue-600 transition-colors">市販水</NuxtLink>
            <NuxtLink to="/compare" class="hover:text-blue-600 transition-colors">比較</NuxtLink>
          </nav>
        </div>
      </div>
    </header>

    <main>
      <slot />
    </main>

    <footer class="bg-gray-800 text-gray-400 text-sm py-8 mt-16">
      <div class="max-w-7xl mx-auto px-4 text-center space-y-2">
        <p class="font-medium text-gray-300">MizuMap — 日本の水道水水質情報マップ</p>
        <p class="text-xs text-gray-500">
          表示データは各自治体の公開情報に基づきます。最新情報は各自治体へご確認ください。
        </p>
      </div>
    </footer>
  </div>
</template>
