<script>
  import { upload, checkHash } from './store'
  import { hashes, hashFile } from './actions/hashes'
  import DropDown from './DropDown.svelte'
  let form, file
// Constants
  const TEXT_FILE = upload.TEXT_FILE
// Calculated values
  $: ready = $hashes?.[TEXT_FILE]?.ready
  $: hash = $hashes?.[TEXT_FILE]?.[0]
  $: hashing = file?.value && !ready
// Handlers
  const handleSubmit = async e => {
    e.preventDefault()
    await checkHash.loadData({ data: { hash }})
    const textParsed = checkHash.textParsed
    await upload.loadAndCheck({ form, textParsed })
  }
  $: stopwordsStr = JSON.stringify($upload.stopwords) || "[]"
</script>

<form action="" enctype="multipart/form-data" bind:this={form}>
  <input name={TEXT_FILE} use:hashFile bind:this={file} type="file">
  <input name="hash" bind:value={hash} type="text" hidden>
  <span class="hashing" hidden={!hashing}>Hashing...</span>
  <DropDown name="lang"/>
  <input name="stopwords" value={stopwordsStr} type="text" hidden>
  <input type="submit" on:click={handleSubmit} disabled={!ready}>
</form>

<style>
  .hashing {
    font-size: 0.8em;
    color: green;
    text-align: left;
  }
</style>
