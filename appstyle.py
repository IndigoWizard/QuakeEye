st_css="""
    <head>
        <title>QuakeEye - Earthquake Data Visualization</title>
    </head>
  <style>
  /*Main app page*/
  /* main page
  .css-ffhzg2 {
    background: rgb(14, 17, 23);
  }*/
  .css-k1ih3n{
      padding: 2rem 1rem 5rem;
  }
  /*Sidebar*/
  .css-1vencpc {
      width: 20vw !important;
      background: #1d4f84;
  }
  .css-1vq4p4l{
      padding: 2rem 1rem;
  }
  .css-5m2qup{
    gap: 1.2rem;
  }
  </style>
"""

map_css = """
{% macro html(this, kwargs) %}
    <head>
        <title>QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari</title>
        
        <!-- Global Meta Tags -->
        <meta itemprop="image" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">
        <meta itemprop="thumbnailUrl" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">
        <link rel="image_src" href="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">
        <link rel="shortcut icon" type="image/x-icon" href="https://cdn-icons-png.flaticon.com/512/2377/2377860.png">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer"/>
        <link rel="stylesheet" href="style.css">

        <!-- LinkediI Meta Tags -->
        <meta property="og:url" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif"/>
        <meta property="og:title" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari"/>
        <meta property="og:description" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari"/>
        <meta property="og:image" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif"/>

        <!-- Facebook Meta Tags -->
        <meta property="og:url" content="https://indigowizard.github.io/QuakeEye/map.html">
        <meta property="og:type" content="website">
        <meta property="og:title" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari">
        <meta property="og:description" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari">
        <meta property="og:image" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">

        <!-- Twitter Meta Tags -->
        <meta name="twitter:card" content="summary_large_image">
        <meta property="twitter:domain" content="https://indigowizard.github.io/QuakeEye/map.html">
        <meta property="twitter:url" content="https://indigowizard.github.io/QuakeEye/map.html">
        <meta name="twitter:title" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari">
        <meta name="twitter:description" content="QuakeEye - Real-Time Earthquake Data Visualization by Ahmed I. Mokhtari">
        <meta name="twitter:image" content="https://user-images.githubusercontent.com/43890965/221388610-ab938380-7c0f-46bc-be71-6ee2031cb6bb.gif">

        <!-- Meta Tags Generated via https://www.opengraph.xyz -->
    </head>
    
    <style>
/* Marker PopUp Box CSS */
        .leaflet-popup-content-wrapper{
            padding: 1px;
            text-align: left;
            border: 4px solid #d7a45d;
            border-radius: 12px;
            /*GLASSMORPHISM EFFECT*/
            background: rgba( 28, 25, 56, 0.25 );
            box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
            backdrop-filter: blur( 4px );
            -webkit-backdrop-filter: blur( 4px );
            border: 4px solid rgba( 215, 164, 93, 0.2 );
        }
        .leaflet-popup-content{
            margin: 13px 24px 13px 20px;
            font-size: 1.2em;
            line-height: 1.3;
            min-height: 1px;
        }
        .popinfo {
            width: max-content;
            border-radius: 5px;
            color: #993200;
        }
        .popinfo h5{
            text-align: center;
        }
        .popinfo span{
            font-weight: bold;
            color: #9d3a00;
        }
        .popinfo b{
            font-weight: 800;
            font-family: bariol;
            font-size: 1.4em;
        }
        .leaflet-popup-tip{
            background: #d7a45d !important;
        }

/* Layer Control Panel CSS */

        .leaflet-control-layers-list {
            width: 14vw;
            min-width: 130px;
            overflow-y: auto;
            overflow-x: hidden;
        }
        .leaflet-control-layers form {
            z-index: 10000;
            overflow-y: auto;
            overflow-x: hidden;
        }
        .leaflet-control-layers-group-label{
            padding: 2px;
            margin: 2px;
            background-color: #d75d5d;
            border: 1px dashed black;
            border-radius: 4px;
            text-align: center;
        }
    </style>

{% endmacro %}
"""
