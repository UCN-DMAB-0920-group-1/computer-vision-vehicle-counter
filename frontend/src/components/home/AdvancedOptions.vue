<template>
  <div class="bg-blue-200 rounded-xl p-3">
    <h1>Advanded options:</h1>

    <div class="grid grid-cols-3 gap-6">
      <div class="col-span-3 sm:col-span-2">
        <label
          for="minimumConfidence"
          class="block text-sm font-medium text-gray-700"
        >
          minimum confidence
        </label>
        <div class="mt-1 flex rounded-md shadow-sm">
          <input
            type="text"
            name="minimumConfidence"
            id="minimumConfidence"
            class="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
            placeholder="0.5"
          />
        </div>
      </div>
    </div>

    <div class="mt-4 space-y-4">
      <div class="flex items-start">
        <div class="flex h-5">
          <input
            id="roi"
            name="roi"
            type="checkbox"
            class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
          />
        </div>
        <div class="ml-3 text-sm">
          <label for="roi" class="font-medium text-gray-700"
            >Region of interest (ROI)</label
          >
          <p class="text-gray-500">
            Set the Region of interest, in the video feed
          </p>
        </div>

        <div class="grid grid-cols-1 gap-4">
          <label
            for="minimumConfidence"
            class="block text-sm font-medium text-gray-700"
          >
            start X
          </label>
          <div class="mt-1 flex rounded-md shadow-sm">
            <input
              type="text"
              name="minimumConfidence"
              id="minimumConfidence"
              class="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
              placeholder="0.5"
            />
          </div>

          <label
            for="minimumConfidence"
            class="block text-sm font-medium text-gray-700"
          >
            max X
          </label>
          <div class="mt-1 flex rounded-md shadow-sm">
            <input
              type="text"
              name="minimumConfidence"
              id="minimumConfidence"
              class="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
              placeholder="0.5"
            />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-4">
          <label
            for="minimumConfidence"
            class="block text-sm font-medium text-gray-700"
          >
            start Y
          </label>
          <div class="mt-1 flex rounded-md shadow-sm">
            <input
              type="text"
              name="minimumConfidence"
              id="minimumConfidence"
              class="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
              placeholder="0.5"
            />
          </div>

          <label
            for="minimumConfidence"
            class="block text-sm font-medium text-gray-700"
          >
            max Y
          </label>
          <div class="mt-1 flex rounded-md shadow-sm">
            <input
              type="text"
              name="minimumConfidence"
              id="minimumConfidence"
              class="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
              placeholder="0.5"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
