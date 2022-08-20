<script>
  import { upload } from './store'
  const OPTIONS = {
    lang: [
      ["en", "English"],
      ["ru", "Русский"],
    ]
  }
  export let name="lang"
  const options = OPTIONS[name]
  export let value=options[0][0]
// Handlers
  const handleChange = e => upload.reset()
</script>

<input {name} bind:value={value} hidden>
<select id="language" bind:value={value} on:change={handleChange}>
  {#each options as [k, v]}
    <option value="{k}">{v}</option>
  {/each}
</select>
