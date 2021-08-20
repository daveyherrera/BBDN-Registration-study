
class EmailBlock:

  def __init__(self):
    pass

  def getEmailBlock(self,first,learn_url,instructor,student,password):

    head="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head>
   <!--[if gte mso 9]>
      <xml>
         <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
         </o:OfficeDocumentSettings>
      </xml>
      <![endif]-->

   <title>Blackboard</title>
   <meta content="text/html; charset=utf-8" http-equiv="Content-type">
   <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport">
   <meta content="IE=edge" http-equiv="X-UA-Compatible">
   <meta content="date=no" name="format-detection">
   <meta content="address=no" name="format-detection">
   <meta content="telephone=no" name="format-detection">
   <meta name="x-apple-disable-message-reformatting"><!--[if !mso]><!-->
   <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,700,700i" rel="stylesheet">
   <link href="https://www.blackboard.com/themes/custom/blackboard/favicon.ico" rel="shortcut icon" type="image/x-icon">
   <!--<![endif]--><!--[if gte mso 9]>
      <style type="text/css" media="all">
         sup { font-size: 100% !important; }
      </style>
   <![endif]-->

      <style media="screen" type="text/css">
          /* Linked Styles */
              body {
          font-family: "Source Sans Pro", sans-serif;
          padding: 0 !important;
          margin: 0 !important;
          display: block !important;
          min-width: 100% !important;
          width: 100% !important;
          background: #f1f1f1;
          -webkit-text-size-adjust: none;
              }

              img {
          -ms-interpolation-mode: bicubic;
          /* Allow smoother rendering of resized image in Internet Explorer */
               }

               p {
          padding: 0 !important;
          margin: 0 !important;
          text-rendering: optimizeLegibility;
              }

              .text {
          color:#0a0a0a;
          font-family: "Source Sans Pro", sans-serif;
          font-size:1rem;
          line-height:1.55rem;
          text-align:left;
          margin-bottom:1rem;
              }
              .text-white {
          color:#ffffff;
          font-family: "Source Sans Pro", sans-serif;
          font-size:1rem;
          line-height:1.55rem;
          text-align:left;
          margin-bottom:1rem;
              }
              .text-header {
          color:#26272c;
          font-family: "Source Sans Pro", sans-serif;
          font-size:12px;
          line-height:16px;
          text-align:left
              }
              .text-header-r {
          color:#26272c;
          font-family: "Source Sans Pro", sans-serif;
          font-size:12px;
          line-height:16px;
          text-align:right
              }

          /* CTA BUTTON */
              .text-button {
          background-color: #f9a21d!important;
          color: #0a0a0a!important;
          background-size: 0 100%;
          background-image: linear-gradient(to left,#ffd191,#ffd191);
          background-repeat: no-repeat;
          transition: background .5s;
          -webkit-transition-duration: 0.5s; /* Safari */
          padding: 13px 48px 13px 48px;
          border-radius: 4px!important;
              }
              .text-button-link {
          color: #0a0a0a!important;
          text-decoration: none;
          font-family: 'Source Sans Pro', sans-serif;
          font-size:18px;
          line-height:21px;
          text-align:center;
          font-weight:bold;
          text-transform:uppercase;
              }
              .text-button:hover, .text-button:focus, .text-button:hover a, .text-button:hover span {
          background-repeat: no-repeat;
          background-size: 100% 100%;
          transition: background .5s;
          color: #0a0a0a!important;
          -webkit-transition-duration: 0.5s; /* Safari */
              }
              .text-button-link:hover, .text-button-link:focus {
          color: #0a0a0a!important;
          text-decoration: none;
              }

          /* LINKS */
         a.link:link, a.link:visited {
         color: #4776BD!important;
         text-decoration: none;
         }
         a.link-u:link, a.link-u:visited {
         color: #4776BD!important;
         text-decoration: underline;
         }
         a.link:hover, a.link:focus,
         a.link-u:hover, a.link-u:focus {
         color: #F9A21D!important;
         }
         a.link2:link, a.link2:visited {
         color: #000001;
         text-decoration: none;
         }
         a.link2-u:link, a.link2-u:visited {
         color: #000001;
         text-decoration: underline;
         }
         a.link-white:link, a.link-white:visited {
         color: #ffffff;
         text-decoration: none;
         }
         a.link-white-u:link, a.link-white-u:visited {
         color: #ffffff;
         text-decoration: underline;
         }
         a.link-white:hover, a.link-white:focus,
         a.link-white-u:hover, a.link-white-u:focus {
         color: #F9A21D!important;
         }
         .text a {
         color: #4776BD;
         text-decoration: underline;
         }
         .text a:hover {
         color: #F9A21D;
         }

          /* SECTIONS */
               .section {
          padding: 40px 40px 40px 40px !important;
          background-color: #ffffff;
               }
               .section-grey {
          padding: 40px 40px 40px 40px !important;
          background-color: #f8f8f8;
               }
               .section-black {
          padding: 40px 40px 40px 40px !important;
          background-color: #0a0a0a;
               }
               .quote {
          padding: 40px 40px 40px 40px !important;
          background-color: #4776BE;
               }

          /* Mobile styles */
               @media only screen and (max-device-width: 480px),only screen and (max-width: 480px) {
               .header {
          padding: 20px 15px 20px 15px !important;
               }
               .mobile-shell {
          width: 100% !important;
          min-width: 100% !important;
               }
               .center {
          margin: 0 auto !important;
               }
               .td {
          width: 100% !important;
          min-width: 100% !important;
               }
               .mobile-br-5 {
          height: 5px !important;
               }
               .mobile-br-10 {
          height: 10px !important;
               }
               .mobile-br-15 {
          height: 15px !important;
               }
               .top-bar {
          padding: 20px 15px 20px 15px !important;
               }
               .header {
          padding: 16px 15px 16px 15px !important;
               }
               .section {
          padding: 40px 15px 40px 15px !important;
          background-color: #ffffff;
               }
               .section-grey {
          padding: 40px 15px 40px 15px !important;
          background-color: #f8f8f8;
               }
               .section-black {
          padding: 40px 15px 40px 15px !important;
          background-color: #0a0a0a;
               }
               .quote {
          padding: 40px 15px 40px 15px !important;
          background-color: #4776BE;
               }
               .footer {
          padding: 20px 15px 30px 15px !important;
               }
               .section-date {
          padding: 20px 15px 20px 15px !important;
               }
               .m-td,
               .hide-for-mobile {
          display: none !important;
          width: 0 !important;
          height: 0 !important;
          font-size: 0 !important;
          line-height: 0 !important;
          min-height: 0 !important;
               }
               .mobile-block {
          display: block !important;
               }
               .text-header,
               .text-header-r,
               .img-m-center {
          text-align: center !important;
               }
               .fluid-img img {
          width: 100% !important;
          max-width: 100% !important;
          height: auto !important;
               }
               .bg {
          background-position: center 0 !important;
               }
               .column,
               .column-top,
               .column-bottom,
               .column-dir {
          float: left !important;
          width: 100% !important;
          display: block !important;
               }
               .w-auto {
          width: auto !important;
               }
               .content-spacing {
          width: 15px !important;
               }
               .text-top,
               .text-top-right,
               .h2-white-center,
               .h3-white-m-center,
               .text-3-white-right {
          text-align: center !important;
               }
               }
   </style>
</head>"""

    body = """
  <body class="body" style="padding:0 !important; margin:0 !important; display:block !important; min-width:100% !important; width:100% !important; background:#f8f8f8; -webkit-text-size-adjust:none">
   <table bgcolor="#F1F1F1" border="0" cellpadding="0" cellspacing="0" width="100%">
      <tbody>
         <tr>
            <td align="center" class="" valign="top">
               <table border="0" cellpadding="0" cellspacing="0" class="mobile-shell" width="600">
                  <tbody>
                     <tr>
                        <td class="td" style="width:600px; min-width:600px; font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; Margin:0">

                           <!-- START Top Bar -->
                           <table border="0" cellpadding="0" cellspacing="0" width="100%">
                              <tbody>
                                 <tr>
                                    <td class="top-bar" style="padding:32px 0px 8px 0px;">
                                       <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                          <tbody>
                                             <tr>
                                                <th class="column-top" style="font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; vertical-align:top; Margin:0" width="">
                                                   <div>
                                                      <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                         <tbody>

                                                            <!-- START Preheader Text -->
                                                            <tr>
                                                               <td class="text-header">
                                                                  All you need to start using your 30-day Blackboard Trial inside.
<div style="display: none; max-height: 0px; overflow: hidden;">
&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
</div>
                                                                  <div class="mobile-br-10" style="font-size:0pt; line-height:0pt;">
                                                                  </div>
                                                               </td>
                                                            </tr>
                                                            <!-- END Preheader Text -->
                                                         </tbody>
                                                      </table>
                                                   </div>
                                                </th>

                                                <th class="column-top" style="font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; vertical-align:top; Margin:0" width="100">
                                                   <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                      <tbody>
                                                         <tr>
                                                            <td class="text-header-r">
                                                               <!--a class="link-u" data-targettype="sysaction" href="https://app.email.blackboard.com/e/es?s=~~eloqua..type--emailfield..syntax--siteid..encodeFor--url~~&e=~~eloqua..type--emailfield..syntax--elqemailsaveguid..encodeFor--url~~&elqTrackId=1352B60E4DDF18321C0347862681ADB0" style="color:#000001; text-decoration:underline" target="_blank">View Online</a-->
                                                            </td>
                                                         </tr>
                                                      </tbody>
                                                   </table>
                                                </th>
                                             </tr>
                                          </tbody>
                                       </table>
                                    </td>
                                 </tr>
                              </tbody>
                           </table>
                           <!-- END Top Bar -->

                           <!-- START Logo -->
                           <span elqid="288" elqtype="DynamicContent" class="remove-absolute" style="display: block"></span>
                          <!-- END Logo -->

    <!-- START Section 1: Opening Pargraphs + CTA Button -->
    <div>
       <table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" width="100%">
          <tbody>
             <tr>
                <td class="section" style="padding:40px 40px 35px 40px;">
                   <table border="0" cellpadding="0" cellspacing="0" width="100%">
                      <tbody>
                         <!-- START Body Text -->
                         <tr>
                            <td style="padding-bottom: 20px;border-bottom: 0;" class="">
                               <div class="text" style="color:#0a0a0a; font-family: 'Source Sans Pro', sans-serif; font-size:16px; line-height:27px; text-align:left; margin-bottom:1rem">
                                  Dear {first},<br>
                                  <br>
                                  Thank you for registering for the <b>Blackboard Trial</b>. Save this e-mail as it contains instructions on how to access your 30-day trial.</div>

                            </td>
                         </tr>
                        <!-- END Body Text -->
                        <tr>
                          <td>
                        <!-- 2 Columns -->
								<table width="100%" cellspacing="0" cellpadding="0" border="0">
								<tbody>
								<tr>
									<td>
										<table width="100%" cellspacing="0" cellpadding="0" border="0">
										<tbody>
										<tr>
											<th width="80" valign="top" class="column" style="font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; Margin:0">
												<table width="100%" cellspacing="0" cellpadding="0" border="0">
												<tbody>
												<tr>
													<td>
														<div class="img-center" style="font-size: 0pt; line-height: 0pt; text-align: left; border-style: none;">
															<img width="80" border="0" src="https://images.email.blackboard.com/EloquaImages/clients/BlackboardInc/%7B11e43398-5bf9-46a2-a8f6-69c34edd50a2%7D_Online_coursework.png" alt="Online Coursework" class="">
														</div>
													</td>
												</tr>
												</tbody>
												</table>
											</th>
											<th width="25" valign="top" class="column" style="font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; Margin:0">
												<table width="100%" cellspacing="0" cellpadding="0" border="0" class="spacer" style="font-size:0pt; line-height:0pt; text-align:center; width:100%; min-width:100%">
												<tbody>
												<tr>
													<td height="20" class="spacer" style="font-size:0pt; line-height:0pt; text-align:center; width:100%; min-width:100%">&nbsp;</td>
												</tr>
												</tbody>
												</table>
											</th>
											<th valign="top" class="column" style="font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; Margin:0">
												<table width="100%" cellspacing="0" cellpadding="0" border="0">
												<tbody>
												<tr>
													<td class="">
														<div class="text" style="color:#0a0a0a; font-family: 'Source Sans Pro', sans-serif; font-size:16px; line-height:27px; text-align:left; margin-bottom:1rem">
                                                          <strong class="">How to access your free 30-day Blackboard Trial:</strong>
														</div>
														<div class="text" style="color:#0a0a0a; font-family: 'Source Sans Pro', sans-serif; font-size:16px; line-height:27px; text-align:left; margin-bottom:1rem">
															 <!--Follow this instructions:--><ul>
                                                          <li>Login through this URL: <a href="https://trial.blackboard.com/?elqTrackId=f12ed86c080c44678505b4d8380d7162&elqTrack=true">trial.blackboard.com</a></li>
                                                          <li>Enter your instructor username: {instructor}</li>
                                                          <li>Enter your student username: {student}</li>
                                                          <li>Enter your password: {password}</li>
                                                          </ul>
														</div>
													</td>
												</tr>
												</tbody>
												</table>
											</th>
										</tr>
										</tbody>
										</table>
										<!--table width="100%" cellspacing="0" cellpadding="0" border="0" class="spacer" style="font-size:0pt; line-height:0pt; text-align:center; width:100%; min-width:100%">
										<tbody>
										<tr>
											<td height="15" class="spacer" style="font-size:0pt; line-height:0pt; text-align:center; width:100%; min-width:100%">&nbsp;</td>
										</tr>
										</tbody>
										</table-->
									</td>
								</tr>
								</tbody>
								</table>
								<!-- END The 2 columns -->

                        		<!-- 2 Columns
								<table width="100%" cellspacing="0" cellpadding="0" border="0">
								<tbody>
								<tr>
									<td>
										<table width="100%" cellspacing="0" cellpadding="0" border="0">
										<tbody>
										<tr>
											<th width="80" valign="top" class="column" style="font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; Margin:0">
												<table width="100%" cellspacing="0" cellpadding="0" border="0">
												<tbody>
												<tr>
													<td>
														<div class="img-center" style="font-size:0pt; line-height:0pt; text-align:left">
															<img width="80" border="0" height="80" src="https://img.en25.com/Web/BlackboardInc/%7Bdf088721-b1b1-4564-95f8-ef8be13bfa36%7D_Administrator.png" alt="Guest" class="">
														</div>
													</td>
												</tr>
												</tbody>
												</table>
											</th>
											<th width="25" valign="top" class="column" style="font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; Margin:0">
												<table width="100%" cellspacing="0" cellpadding="0" border="0" class="spacer" style="font-size:0pt; line-height:0pt; text-align:center; width:100%; min-width:100%">
												<tbody>
												<tr>
													<td height="20" class="spacer" style="font-size:0pt; line-height:0pt; text-align:center; width:100%; min-width:100%">&nbsp;</td>
												</tr>
												</tbody>
												</table>
											</th>
											<th valign="top" class="column" style="font-size:0pt; line-height:0pt; padding:0; margin:0; font-weight:normal; Margin:0">
												<table width="100%" cellspacing="0" cellpadding="0" border="0">
												<tbody>
												<tr>
													<td class="">
														<div class="text" style="color:#0a0a0a; font-family: 'Source Sans Pro', sans-serif; font-size:16px; line-height:27px; text-align:left; margin-bottom:1rem">
                                                          <strong class="">Share the access link for participants:</strong> <a href="https://s2376.t.eloqua.com/e/f2.aspx?elqFormName=CollabFreeTrial&elqSiteID=2376&Description=Clicked%20to%20access%20guest%20room%20on%20Collaborate%20trial&emailAddress=~~eloqua..type--emailfield..syntax--EmailAddress..innerText--EmailAddress..encodeFor--url~~&Link=~~eloqua..type--emailfield..syntax--INTL_2016_CROSS_CollabTrial_GuestLink_Viali1..innerText--INTL_2016_CROSS_CollabTrial_GuestLink_Viali1..encodeFor--url~~&elqTrackId=f98f6d3cafd3404093616b79d059be7f"><span class="eloquaemail">INTL_2016_CROSS_CollabTrial_GuestLink_Viali1</span></a>
														</div>
														<div class="text" style="color:#0a0a0a; font-family: 'Source Sans Pro', sans-serif; font-size:16px; line-height:27px; text-align:left; margin-bottom:1rem">
															 Guest participants have limited access to features within Collaborate. Share this link with your colleagues to start a meeting today!
														</div>
													</td>
												</tr>
												</tbody>
												</table>
											</th>
										</tr>
										</tbody>
										</table>
									</td>
								</tr>
								</tbody>
								</table>
								<!-- END The 2 columns -->
                     </td>
            </tr>
                     </tbody>
                  </table>
               </td>
            </tr>
          </tbody>
       </table>
      <!-- START Section 1: Opening Pargraphs + CTA Button -->

      <!-- START Section 2: Articles -->
       <table bgcolor="#F8F8F8" border="0" cellpadding="0" cellspacing="0" width="100%">
          <tbody>
             <tr>
                <td class="section-grey" style="padding:20px 40px 20px 40px;">
                   <table border="0" cellpadding="0" cellspacing="0" width="100%">
                      <tbody>
                         <tr>
                            <td>
                               <div class="text" style="color:0a0a0a; font-family: 'Source Sans Pro', sans-serif; font-size:16px; line-height:27px; text-align:left">								30 days will go by fast so, to be sure to make the most of your trial, we’ll provide tips, hacks and insights along the way.<br><br>
                                 <a href="https://www.blackboard.com/teaching-learning/learning-management/blackboard-learn?elqTrackId=724977b9342f4e9bb265105e0faa196e&elqTrack=true" data-targettype="webpage" title="Help Portal"><strong>Want more information about Blackboard Learn?</strong></a>

                                 <br><br><b>Looking for help?

                                 </b><br>
Check out our&nbsp;<a href="https://help.blackboard.com/Learn?elqTrackId=c817dc7434f64d0a922d47417464c0a4&elqTrack=true" data-targettype="webpage" title="Help Portal"><strong>help portal</strong></a>.
                              </div>
                            </td>
                         </tr>
                      </tbody>
                   </table>
                </td>
             </tr>
          </tbody>
       </table>
    </div>
	<!-- END Section 3: Closing Paragraph -->
                           <!-- ******** DO NOT REMOVE THIS SECTION ******** -->
                           <!-- START Footer Section -->
                           <span elqid="421" elqtype="DynamicContent" class="remove-absolute" style="display: block"></span>
                          <!-- FOOTER SECTION END -->
                        </td>
                     </tr>
                  </tbody>
               </table>
            </td>
         </tr>
      </tbody>
   </table>
</body></html>""".format(first=first,learn_url=learn_url,instructor=instructor,student=student,password=password)

    return(head + body)
