<script>
  import { HOST } from './utils/api'
  import { upload } from './store'
  $: loading = $upload.loading
  $: wcloud = $upload.wcloud
  $: error = $upload.error
</script>

{#if loading}
  <p class="loading ">Loading...</p>
{/if}

{#if error}
  <p>{error}</p>
{/if}

{#if wcloud}
  <img src={HOST}/{wcloud} alt="Word cloud">
{/if}

<style>
  .loading {
    color: green;
  }
</style>