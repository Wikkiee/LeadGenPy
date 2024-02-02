def generate_embedded_email_content(content):
    contents = str(content).split(",", 1)
    contents[0] = contents[0].replace("Dear","Hi",1)
    contents[1] = contents[1].replace("\n","<br/>")

    embedded_htm_email = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
  <title></title>

  <style type="text/css">
    @media only screen and (min-width: 620px) {
      .u-row {
        width: 600px !important;
      }

      .u-row .u-col {
        vertical-align: top;
      }

      .u-row .u-col-33p33 {
        width: 199.98px !important;
      }

      .u-row .u-col-100 {
        width: 600px !important;
      }

    }

    @media (max-width: 620px) {
      .u-row-container {
        max-width: 100% !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
      }

      .u-row .u-col {
        min-width: 320px !important;
        max-width: 100% !important;
        display: block !important;
      }

      .u-row {
        width: 100% !important;
      }

      .u-col {
        width: 100% !important;
      }

      .u-col>div {
        margin: 0 auto;
      }
    }

    body {
      margin: 0;
      padding: 0;
    }

    table,
    tr,
    td {
      vertical-align: top;
      border-collapse: collapse;
    }

    p {
      margin: 0;
    }

    .ie-container table,
    .mso-container table {
      table-layout: fixed;
    }

    * {
      line-height: inherit;
    }

    a[x-apple-data-detectors='true'] {
      color: inherit !important;
      text-decoration: none !important;
    }

    table,
    td {
      color: #000000;
    }

    #u_body a {
      color: #0000ee;
      text-decoration: underline;
    }

    @media (max-width: 480px) {
      #u_content_heading_3 .v-font-size {
        font-size: 23px !important;
      }

      #u_content_image_1 .v-src-width {
        width: auto !important;
      }

      #u_content_image_1 .v-src-max-width {
        max-width: 100% !important;
      }

      #u_content_text_1 .v-container-padding-padding {
        padding: 60px 15px 20px !important;
      }

      #u_content_text_1 .v-text-align {
        text-align: center !important;
      }

      #u_content_button_1 .v-size-width {
        width: 45% !important;
      }

      #u_row_3 .v-row-background-image--inner {
        background-position: center top !important;
        background-repeat: no-repeat !important;
      }

      #u_row_3 .v-row-background-image--outer {
        background-image: url('images/image-7.jpeg') !important;
        background-position: center top !important;
        background-repeat: no-repeat !important;
      }

      #u_row_3.v-row-background-image--outer {
        background-image: url('images/image-7.jpeg') !important;
        background-position: center top !important;
        background-repeat: no-repeat !important;
      }

      #u_content_image_3 .v-container-padding-padding {
        padding: 30px 10px 0px !important;
      }

      #u_content_image_3 .v-src-width {
        width: auto !important;
      }

      #u_content_image_3 .v-src-max-width {
        max-width: 35% !important;
      }

      #u_content_social_2 .v-container-padding-padding {
        padding: 15px 10px 10px !important;
      }

      #u_content_heading_1 .v-container-padding-padding {
        padding: 15px 10px 0px !important;
      }

      #u_content_text_2 .v-container-padding-padding {
        padding: 5px 80px 0px !important;
      }

      #u_content_heading_2 .v-container-padding-padding {
        padding: 25px 10px 0px !important;
      }

      #u_content_text_3 .v-container-padding-padding {
        padding: 5px 10px 30px !important;
      }
    }
  </style>"""+f"""
  <!--[if !mso]><!-->
  <link href="https://fonts.googleapis.com/css?family=Playfair+Display:400,700&display=swap" rel="stylesheet"
    type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Raleway:400,700&display=swap" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Raleway:400,700&display=swap" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Playfair+Display:400,700&display=swap" rel="stylesheet"
    type="text/css"><!--<![endif]-->

</head>

<body class="clean-body u_body"
  style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #deeafa;color: #000000">
  <table id="u_body"
    style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #deeafa;width:100%"
    cellpadding="0" cellspacing="0">
    <tbody>
      <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">



          <div class="u-row-container v-row-background-image--outer" style="padding: 0px;background-color: transparent">
            <div class="u-row"
              style="margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
              <div class="v-row-background-image--inner"
                style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">

                <div class="u-col u-col-100"
                  style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
                  <div style="height: 100%;width: 100% !important;">
                    <!--[if (!mso)&(!IE)]><!-->
                    <div
                      style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">
                      <!--<![endif]-->

                      <table id="u_content_heading_3" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:35px 10px 0px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <!--[if mso]><table width="100%"><tr><td><![endif]-->
                              <h1 class="v-text-align v-font-size"
                                style="margin: 0px; line-height: 130%; text-align: center; word-wrap: break-word; font-family: 'Playfair Display',serif; font-size: 40px; font-weight: 400;">
                                A New Opportunity to<br /><strong>Grow Your Business</strong></h1>
                              <!--[if mso]></td></tr></table><![endif]-->

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <table id="u_content_image_1" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                  <td class="v-text-align" style="padding-right: 0px;padding-left: 0px;" align="center">

                                    <img align="center" border="0" src="https://i.imgur.com/5HYVjRP.jpeg"
                                      alt="Illustration" title="Illustration"
                                      style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 76%;max-width: 456px;"
                                      width="456" class="v-src-width v-src-max-width" />

                                  </td>
                                </tr>
                              </table>

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <!--[if (!mso)&(!IE)]><!-->
                    </div><!--<![endif]-->
                  </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
              </div>
            </div>
          </div>





          <div class="u-row-container v-row-background-image--outer" style="padding: 0px;background-color: transparent">
            <div class="u-row"
              style="margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
              <div class="v-row-background-image--inner"
                style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
                <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-image--outer" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-background-image--inner" style="background-color: transparent;"><![endif]-->

                <!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px 0px 60px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-100"
                  style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
                  <div
                    style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                    <!--[if (!mso)&(!IE)]><!-->
                    <div
                      style="box-sizing: border-box; height: 100%; padding: 0px 0px 60px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                      <!--<![endif]-->

                      <table id="u_content_text_1" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:60px 30px 20px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <div class="v-text-align v-font-size"
                                style="font-size: 14px; line-height: 160%; text-align: justify; word-wrap: break-word;">
                                <p style="font-size: 14px; line-height: 160%; text-align: center;"><strong><span
                                      style="font-family: 'Playfair Display', serif; font-size: 16px; line-height: 25.6px;"><span
                                        style="line-height: 25.6px; font-size: 16px;">{contents[0]}</span></span></strong></p>
                                <p style="font-size: 14px; line-height: 160%; text-align: center;"> </p>
                                <p style="font-size: 14px; line-height: 160%; text-align: justify;">{contents[1]}</p>
                              </div>

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <table id="u_content_button_1" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Raleway',sans-serif;"
                              align="left">
                              <div class="v-text-align" align="center">
                                <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://github.com/Wikkiee/LeadGenPy" style="height:37px; v-text-anchor:middle; width:162px;" arcsize="11%"  stroke="f" fillcolor="#001847"><w:anchorlock/><center style="color:#FFFFFF;"><![endif]-->
                                <a href="https://github.com/Wikkiee/LeadGenPy" target="_blank"
                                  class="v-button v-size-width v-font-size"
                                  style="box-sizing: border-box;display: inline-block;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #FFFFFF; background-color: #001847; border-radius: 4px;-webkit-border-radius: 4px; -moz-border-radius: 4px; width:28%; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;font-size: 14px;">
                                  <span style="display:block;padding:10px 20px;line-height:120%;">Learn More</span>
                                </a>
                                <!--[if mso]></center></v:roundrect><![endif]-->
                              </div>

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <!--[if (!mso)&(!IE)]><!-->
                    </div><!--<![endif]-->
                  </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
              </div>
            </div>
          </div>





          <!--[if gte mso 9]>
      <table cellpadding="0" cellspacing="0" border="0" style="margin: 0 auto;min-width: 320px;max-width: 600px;">
        <tr>
          <td background="https://cdn.templates.unlayer.com/assets/1656669960135-572430.jpg" valign="top" width="100%">
      <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width: 600px;">
        <v:fill type="frame" src="https://cdn.templates.unlayer.com/assets/1656669960135-572430.jpg" /><v:textbox style="mso-fit-shape-to-text:true" inset="0,0,0,0">
      <![endif]-->

          <div id="u_row_3" class="u-row-container v-row-background-image--outer"
            style="padding: 0px;background-image: url('images/image-6.jpeg');background-repeat: no-repeat;background-position: center top;background-color: #000000">
            <div class="u-row"
              style="margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
              <div class="v-row-background-image--inner"
                style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
                <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-image--outer" style="padding: 0px;background-image: url('images/image-6.jpeg');background-repeat: no-repeat;background-position: center top;background-color: #000000;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-background-image--inner" style="background-color: transparent;"><![endif]-->

                <!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #000000;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-33p33"
                  style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                  <div
                    style="background-color: #000000;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                    <!--[if (!mso)&(!IE)]><!-->
                    <div
                      style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                      <!--<![endif]-->

                      <table id="u_content_image_3" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:47px 10px 0px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                  <td class="v-text-align" style="padding-right: 0px;padding-left: 0px;" align="center">

                                    <img align="center" border="0" src="https://camo.githubusercontent.com/a0bb8b25ceb04a3ec0a777f80f9a80552ac1c759c30441deb8aaae9273ac430f/68747470733a2f2f692e696d6775722e636f6d2f764f574c757a592e706e67" alt="Logo"
                                      title="Logo"
                                      style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 65%;max-width: 117px;"
                                      width="117" class="v-src-width v-src-max-width" />

                                  </td>
                                </tr>
                              </table>

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <table id="u_content_social_2" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 52px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <div align="center">
                                <div style="display: table; max-width:140px;">
                                  <!--[if (mso)|(IE)]><table width="140" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-collapse:collapse;" align="center"><table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse; mso-table-lspace: 0pt;mso-table-rspace: 0pt; width:140px;"><tr><![endif]-->


                                  <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 15px;" valign="top"><![endif]-->
                                  <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32"
                                    style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 15px">
                                    <tbody>
                                      <tr style="vertical-align: top">
                                        <td align="left" valign="middle"
                                          style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
                                          <a href="https://facebook.com/" title="Facebook" target="_blank">
                                            <img src="https://i.imgur.com/KS1oaw7.png" alt="Facebook" title="Facebook"
                                              width="32"
                                              style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important">
                                          </a>
                                        </td>
                                      </tr>
                                    </tbody>
                                  </table>
                                  <!--[if (mso)|(IE)]></td><![endif]-->

                                  <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 15px;" valign="top"><![endif]-->
                                  <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32"
                                    style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 15px">
                                    <tbody>
                                      <tr style="vertical-align: top">
                                        <td align="left" valign="middle"
                                          style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
                                          <a href="https://twitter.com/" title="Twitter" target="_blank">
                                            <img src="https://i.imgur.com/KS1oaw7.png" alt="Twitter" title="Twitter"
                                              width="32"
                                              style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important">
                                          </a>
                                        </td>
                                      </tr>
                                    </tbody>
                                  </table>
                                  <!--[if (mso)|(IE)]></td><![endif]-->

                                  <!--[if (mso)|(IE)]><td width="32" style="width:32px; padding-right: 0px;" valign="top"><![endif]-->
                                  <table align="left" border="0" cellspacing="0" cellpadding="0" width="32" height="32"
                                    style="width: 32px !important;height: 32px !important;display: inline-block;border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;margin-right: 0px">
                                    <tbody>
                                      <tr style="vertical-align: top">
                                        <td align="left" valign="middle"
                                          style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
                                          <a href="https://linkedin.com/" title="LinkedIn" target="_blank">
                                            <img src="https://i.imgur.com/KpodPo5.png" alt="LinkedIn" title="LinkedIn"
                                              width="32"
                                              style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: block !important;border: none;height: auto;float: none;max-width: 32px !important">
                                          </a>
                                        </td>
                                      </tr>
                                    </tbody>
                                  </table>
                                  <!--[if (mso)|(IE)]></td><![endif]-->


                                  <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
                                </div>
                              </div>

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <!--[if (!mso)&(!IE)]><!-->
                    </div><!--<![endif]-->
                  </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #000000;width: 200px;padding: 0px 0px 14px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-33p33"
                  style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                  <div
                    style="background-color: #000000;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                    <!--[if (!mso)&(!IE)]><!-->
                    <div
                      style="box-sizing: border-box; height: 100%; padding: 0px 0px 14px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                      <!--<![endif]-->

                      <table id="u_content_heading_1" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:50px 10px 0px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <!--[if mso]><table width="100%"><tr><td><![endif]-->
                              <h1 class="v-text-align v-font-size"
                                style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-family: 'Raleway',sans-serif; font-size: 18px; font-weight: 400;">
                                <strong>About Us</strong>
                              </h1>
                              <!--[if mso]></td></tr></table><![endif]-->

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <table id="u_content_text_2" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:5px 10px 20px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <div class="v-text-align v-font-size"
                                style="font-size: 14px; color: #ffffff; line-height: 160%; text-align: center; word-wrap: break-word;">
                                <p style="font-size: 14px; line-height: 160%;">Leadgenpy✨ : Transform lead generation by extracting Google Maps business details with Selenium, processing data, and dynamically generating personalized messages using Chat GPT API. .</p>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <!--[if (!mso)&(!IE)]><!-->
                    </div><!--<![endif]-->
                  </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]><td align="center" width="200" style="background-color: #000000;width: 200px;padding: 0px 0px 14px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-33p33"
                  style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
                  <div
                    style="background-color: #000000;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                    <!--[if (!mso)&(!IE)]><!-->
                    <div
                      style="box-sizing: border-box; height: 100%; padding: 0px 0px 14px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                      <!--<![endif]-->

                      <table id="u_content_heading_2" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:50px 10px 0px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <!--[if mso]><table width="100%"><tr><td><![endif]-->
                              <h1 class="v-text-align v-font-size"
                                style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-family: 'Raleway',sans-serif; font-size: 18px; font-weight: 400;">
                                <strong>Contact Us</strong>
                              </h1>
                              <!--[if mso]></td></tr></table><![endif]-->

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <table id="u_content_text_3" style="font-family:'Raleway',sans-serif;" role="presentation"
                        cellpadding="0" cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:5px 10px 20px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <div class="v-text-align v-font-size"
                                style="font-size: 14px; color: #ffffff; line-height: 160%; text-align: center; word-wrap: break-word;">
                                <p style="font-size: 14px; line-height: 160%;">Your Street 12, 34567 City</p>
                                <p style="font-size: 14px; line-height: 160%;">info@example.com </p>
                                <p style="font-size: 14px; line-height: 160%;">(+1) 123 456 789</p>
                              </div>

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <!--[if (!mso)&(!IE)]><!-->
                    </div><!--<![endif]-->
                  </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
              </div>
            </div>
          </div>

          <!--[if gte mso 9]>
      </v:textbox></v:rect>
    </td>
    </tr>
    </table>
    <![endif]-->
          <div class="u-row-container v-row-background-image--outer" style="padding: 0px;background-color: transparent">
            <div class="u-row"
              style="margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
              <div class="v-row-background-image--inner"
                style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
                <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-image--outer" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-background-image--inner" style="background-color: transparent;"><![endif]-->

                <!--[if (mso)|(IE)]><td align="center" width="600" style="background-color: #deeafa;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
                <div class="u-col u-col-100"
                  style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
                  <div
                    style="background-color: #deeafa;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                    <!--[if (!mso)&(!IE)]><!-->
                    <div
                      style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
                      <!--<![endif]-->

                      <table style="font-family:'Raleway',sans-serif;" role="presentation" cellpadding="0"
                        cellspacing="0" width="100%" border="0">
                        <tbody>
                          <tr>
                            <td class="v-container-padding-padding"
                              style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:'Raleway',sans-serif;"
                              align="left">

                              <div class="v-text-align v-font-size"
                                style="font-size: 14px; line-height: 140%; text-align: center; word-wrap: break-word;">
                                <p style="font-size: 14px; line-height: 140%;"><span
                                    style="font-family: Raleway, sans-serif; font-size: 14px; line-height: 19.6px;">2024
                                    © All Rights Reserved</span></p>
                              </div>

                            </td>
                          </tr>
                        </tbody>
                      </table>

                      <!--[if (!mso)&(!IE)]><!-->
                    </div><!--<![endif]-->
                  </div>
                </div>
                <!--[if (mso)|(IE)]></td><![endif]-->
                <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
              </div>
            </div>
          </div>



          <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
        </td>
      </tr>
    </tbody>
  </table>
  <!--[if mso]></div><![endif]-->
  <!--[if IE]></div><![endif]-->
</body>

</html>
    
    """
    return embedded_htm_email