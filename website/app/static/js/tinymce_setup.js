tinymce.init({
    selector: 'textarea#full-featured',
    //调用放在langs文件夹内的语言包
    language:'zh_CN',
    //
    plugins: 'print preview fullpage powerpaste casechange importcss code tinydrive searchreplace directionality visualblocks visualchars fullscreen image link codesample table charmap hr insertdatetime advlist lists checklist wordcount tinymcespellchecker a11ychecker imagetools textpattern noneditable formatpainter permanentpen pageembed charmap tinycomments mentions quickbars linkchecker emoticons advtable',
    imagetools_cors_hosts: ['picsum.photos'],


    menubar: 'file edit view insert format tools',
    toolbar: 'fullscreen preview print searchreplace | undo redo | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | checklist | a11ycheck ltr rtl | forecolor backcolor casechange permanentpen formatpainter removeformat | bold italic underline strikethrough | charmap emoticons insertdatetime hr | insertfile image table link codesample | showcomments addcomment',

    // 为图像属性编辑窗口添加高级属性，可以自定义图片的css样式（内置style）、边距（margin）和边框（border）
    image_advtab: false,
    importcss_append: true,

    // 指定上传到服务器的URL
    images_upload_url: '/upload',
    images_upload_base_path: 'http://q7u6l89tx.bkt.clouddn.com/', // 上传文件的基本路径
    convert_urls: false, // 相对路径
    // 该选项可以让你配置调用images_upload_url时是否应用cookies等跨域凭证
    images_upload_credentials: true,
    height: 600,
    image_caption: true,
    quickbars_selection_toolbar: 'bold italic underline strikethrough | forecolor backcolor casechange permanentpen formatpainter removeformat | h1 h2 h3 ',
    quickbars_insert_toolbar: 'image table codesample',
    toolbar_drawer: 'sliding',
    spellchecker_dialog: true,
    tinycomments_mode: 'embedded'
 });