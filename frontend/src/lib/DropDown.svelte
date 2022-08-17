<script>
  const OPTIONS = {
    lang: [
      ["en", "English"],
      ["ru", "Русский"],
    ]
  }
  export let name="lang"
  const options = OPTIONS[name]
  export let value=options[0][0]
</script>

<input {name} {value} hidden>
<select {name} id="language" bind:value={value}>
  {#each options as [value, text]}
    <option value="{value}">{text}</option>
  {/each}
</select>
