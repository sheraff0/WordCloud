<script>
  import UploadForm from './lib/UploadForm.svelte'
  import StopWords from './lib/StopWords.svelte'
  import WordCloud from './lib/WordCloud.svelte'
</script>

<main>
  <div>
    <p>Upload text file (TXT, XML (incl. HTML), PDF)</p>
  </div>
  <h1>Word Cloud</h1>

  <div class="card">
    <WordCloud/>
  </div>

  <UploadForm/>

  <StopWords/>
</main>
