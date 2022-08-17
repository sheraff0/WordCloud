<script>
  import { HOST } from './api'
  import { upload } from './store'
  $: loading = $upload.loading
  $: data = ($upload.data || {})
  $: wcloud = data.wcloud
  $: error = $upload.error
</script>

{#if loading}
  <p>Loading...</p>
{/if}

{#if error}
  <p>{error}</p>
{/if}

{#if wcloud}
  <img src={HOST}/{wcloud} alt="Word cloud">
{/if}
