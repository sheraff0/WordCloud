<script>
  import { upload } from './store'
  import DropDown from './DropDown.svelte'
  let form
// Handlers
  const handleSubmit = async e => {
    e.preventDefault()
    await upload.loadAndCheck({ form })
  }
  $: stopwordsStr = JSON.stringify($upload.stopwords) || "[]"
</script>

<form action="" enctype="multipart/form-data" bind:this={form}>
  <input name="text_file" type="file">
  <DropDown name="lang"/>
  <input name="stopwords" value={stopwordsStr} type="text" hidden>
  <input type="submit" on:click={handleSubmit}>
</form>
