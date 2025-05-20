<template>
  <div class="pdf-container">
    <h2>{{ getPdfName() }}</h2>
    
    <iframe :src="pdfSrc" class="pdf-frame"></iframe>
  </div>
</template>

<script>
export default {
  props: {
    pdfSrc: {
      type: String,
      required: true
    }
  },
  methods: {
    getPdfName() {
      // Extract the PDF name from the URL path
      const parts = this.pdfSrc.split('/');
      const filename = parts[parts.length - 1];
      // Convert filename to readable format (remove underscores, .pdf, etc.)
      return filename
          .replace('.pdf', '')
          .split('_')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ');
    }
  }
}
</script>

<style scoped>
.pdf-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

h2 {
  margin-bottom: 10px;
  text-align: center;
}

.pdf-frame {
  width: 100%;
  height: 600px;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>