from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.header import Header
import psycopg2.extensions
import psycopg2
import smtplib
import pickle
import select
import os


EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

db_conn = psycopg2.connect(
    host = "localhost",
    port = "6432",
    dbname = "server",
    user = "hideyoshi",
    password = "vhnb2901"
)

db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
db = db_conn.cursor()

db.execute('LISTEN novo_pedido')

while 1:

    if not select.select([db_conn], [], [], 5) == ([], [], []):

        db_conn.poll()

        while db_conn.notifies:

            notify = db_conn.notifies.pop()
            id_pedido, c_cpf, id_servico, quantidade, valor_total, date = notify.payload.replace('(','').replace(')','').split(',')

            year,month,day = date.replace('"','').split()[0].split('-')
            hour,minute,sec = date.replace('"','').split()[1].split(':')
            sec = sec.split('.')[0]
            date = datetime(int(year),int(month),int(day),int(hour),int(minute),int(sec))

            months = [
                "Janeiro",
                "Fevereiro",
                "Março",
                "Abril",
                "Maio",
                "Junho",
                "Julho",
                "Augosto",
                "Setembro",
                "Outubro",
                "Novembro",
                "Dezembro"]

            month = months[date.month]

            week = [
                "Segunda",
                "Terça",
                "Quarta",
                "Quinta",
                "Sexta",
                "Sábado",
                "Domingo"]

            dow = week[date.weekday()]

            db.execute('SELECT DISTINCT nome FROM cliente, pedido WHERE cliente.cpf = pedido.cpf and pedido.id ='+id_pedido+';')
            c_nome = str(db.fetchall()).replace('[','').replace('(','').replace(')','').replace(']','').replace(',','').replace("'",'')
            db.execute('SELECT DISTINCT email FROM cliente, pedido WHERE cliente.cpf = pedido.cpf and pedido.id ='+id_pedido+';')
            c_email = str(db.fetchall()).replace('[','').replace('(','').replace(')','').replace(']','').replace(',','').replace("'",'')
            db.execute('SELECT DISTINCT nome FROM servico, pedido WHERE servico.id = id_servico AND pedido.id = '+id_pedido+';')
            p_nome = str(db.fetchall()).replace('[','').replace('(','').replace(')','').replace(']','').replace(',','').replace("'",'')
            db.execute("SELECT DISTINCT endereco.logradouro,endereco.complemento,endereco.numero,endereco.cidade,' - ',endereco.estado FROM endereco, cliente, pedido WHERE cliente.cpf = pedido.cpf AND cliente.id_endereco = endereco.id AND pedido.id = "+id_pedido+";")
            endereco = str(db.fetchall()).replace('[','').replace('(','').replace(')','').replace(']','').replace(',','').replace("'",'')

            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = 'Compra realizada com Sucesso'
            msgRoot['From'] = EMAIL_ADDRESS
            msgRoot['To'] = c_email
            message = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<!--[if gte mso 9]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<meta content="width=device-width" name="viewport"/>
<!--[if !mso]><!-->
<meta content="IE=edge" http-equiv="X-UA-Compatible"/>
<!--<![endif]-->
<title></title>
<!--[if !mso]><!-->
<link href="https://fonts.googleapis.com/css?family=Oswald" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Merriweather" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet" type="text/css"/>
<link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro" rel="stylesheet" type="text/css"/>
<!--<![endif]-->
<style type="text/css">
        body {
            margin: 0;
            padding: 0;
        }

        table,
        td,
        tr {
            vertical-align: top;
            border-collapse: collapse;
        }

        * {
            line-height: inherit;
        }

        a[x-apple-data-detectors=true] {
            color: inherit !important;
            text-decoration: none !important;
        }
    </style>
<style id="media-query" type="text/css">
        @media (max-width: 670px) {

            .block-grid,
            .col {
                min-width: 320px !important;
                max-width: 100% !important;
                display: block !important;
            }

            .block-grid {
                width: 100% !important;
            }

            .col {
                width: 100% !important;
            }

            .col>div {
                margin: 0 auto;
            }

            img.fullwidth,
            img.fullwidthOnMobile {
                max-width: 100% !important;
            }

            .no-stack .col {
                min-width: 0 !important;
                display: table-cell !important;
            }

            .no-stack.two-up .col {
                width: 50% !important;
            }

            .no-stack .col.num4 {
                width: 33% !important;
            }

            .no-stack .col.num8 {
                width: 66% !important;
            }

            .no-stack .col.num4 {
                width: 33% !important;
            }

            .no-stack .col.num3 {
                width: 25% !important;
            }

            .no-stack .col.num6 {
                width: 50% !important;
            }

            .no-stack .col.num9 {
                width: 75% !important;
            }

            .video-block {
                max-width: none !important;
            }

            .mobile_hide {
                min-height: 0px;
                max-height: 0px;
                max-width: 0px;
                display: none;
                overflow: hidden;
                font-size: 0px;
            }

            .desktop_hide {
                display: block !important;
                max-height: none !important;
            }
        }
    </style>
</head>
<body class="clean-body" style="margin: 0; padding: 0; -webkit-text-size-adjust: 100%; background-color: #482c71;">
<!--[if IE]><div class="ie-browser"><![endif]-->
<table bgcolor="#482c71" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="table-layout: fixed; vertical-align: top; min-width: 320px; Margin: 0 auto; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #482c71; width: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top;" valign="top">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color:#482c71"><![endif]-->
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:transparent;width:650px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 650px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div class="mobile_hide">
<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" height="15" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid transparent; height: 15px; width: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td height="15" style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</div>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:transparent;width:650px; border-top: 1px solid #C879F1; border-left: 1px solid #C879F1; border-bottom: 0px solid transparent; border-right: 1px solid #C879F1;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:10px; padding-bottom:0px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 648px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:1px solid #C879F1; border-left:1px solid #C879F1; border-bottom:0px solid transparent; border-right:1px solid #C879F1; padding-top:10px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div align="center" class="img-container center autowidth fixedwidth" style="padding-right: 15px;padding-left: 15px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 15px;padding-left: 15px;" align="center"><![endif]--><img align="center" alt="Image" border="0" class="center autowidth fixedwidth" src="cid:swirls_1.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 618px; display: block;" title="Image" width="618"/>
<div style="font-size:1px;line-height:20px"> </div>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:transparent;width:650px; border-top: 0px solid transparent; border-left: 1px solid #C879F1; border-bottom: 0px solid transparent; border-right: 1px solid #C879F1;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:5px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 648px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:1px solid #C879F1; border-bottom:0px solid transparent; border-right:1px solid #C879F1; padding-top:0px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div align="center" class="img-container center fixedwidth" style="padding-right: 0px;padding-left: 0px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="center"><![endif]--><img align="center" alt="Image" border="0" class="center fixedwidth" src="cid:logoflower.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 259px; display: block;" title="Image" width="259"/>
<div style="font-size:1px;line-height:20px"> </div>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:transparent;width:650px; border-top: 0px solid transparent; border-left: 1px solid #C879F1; border-bottom: 0px solid transparent; border-right: 1px solid #C879F1;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:40px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 648px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:1px solid #C879F1; border-bottom:0px solid transparent; border-right:1px solid #C879F1; padding-top:5px; padding-bottom:40px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 1px dotted #C879F1; width: 95%;" valign="top" width="95%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 30px; padding-bottom: 15px; font-family: serif"><![endif]-->
<div style="color:#E3E3E3;font-family:'Merriwheater', 'Georgia', serif;line-height:1.5;padding-top:30px;padding-right:40px;padding-bottom:15px;padding-left:40px;">
<div style="line-height: 1.5; font-size: 12px; font-family: 'Merriwheater', 'Georgia', serif; color: #E3E3E3; mso-line-height-alt: 18px;">
<p style="line-height: 1.5; word-break: break-word; text-align: center; font-family: Merriwheater, Georgia, serif; font-size: 30px; mso-line-height-alt: 45px; margin: 0;"><span style="font-size: 30px; color: #00ad99;">SUA RESERVA</span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 5px; padding-bottom: 20px; font-family: 'Trebuchet MS', Tahoma, sans-serif"><![endif]-->
<div style="color:#E3E3E3;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:1.5;padding-top:5px;padding-right:40px;padding-bottom:20px;padding-left:40px;">
<div style="font-size: 12px; line-height: 1.5; font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; color: #E3E3E3; mso-line-height-alt: 18px;">
<p style="font-size: 20px; line-height: 1.5; text-align: center; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 30px; margin: 0;"><span style="font-size: 20px;"><span style="font-size: 18px;">"""+dow+", "+day+" "+month+" "+year+"""</span><br/><span style="font-size: 18px;">Serviço: """+p_nome+"""</span><br/><span style="font-size: 18px;">Duração: """+date.strftime("%H:%M")+" - "+(date+timedelta(hours=2)).strftime("%H:%M")+"""</span><br/></span></p>

<div style="color:#E3E3E3;font-family:'Merriwheater', 'Georgia', serif;line-height:1.5;padding-top:30px;padding-right:40px;padding-bottom:15px;padding-left:40px;">
<div style="line-height: 1.5; font-size: 12px; font-family: 'Merriwheater', 'Georgia', serif; color: #E3E3E3; mso-line-height-alt: 18px;">
<p style="line-height: 1.5; word-break: break-word; text-align: center; font-family: Merriwheater, Georgia, serif; font-size: 30px; mso-line-height-alt: 45px; margin: 0;"><span style="font-size: 30px; color: #00ad99;">VALOR</span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 5px; padding-bottom: 20px; font-family: 'Trebuchet MS', Tahoma, sans-serif"><![endif]-->
<div style="color:#E3E3E3;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:1.5;padding-top:5px;padding-right:40px;padding-bottom:20px;padding-left:40px;">
<div style="font-size: 12px; line-height: 1.5; font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; color: #E3E3E3; mso-line-height-alt: 18px;">
<p style="font-size: 20px; line-height: 1.5; text-align: center; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 30px; margin: 0;"><span style="font-size: 20px;"><span style="font-size: 18px;">R$ """+valor_total+"""</span><br/></span></p>    
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:transparent;width:650px; border-top: 0px solid transparent; border-left: 1px solid #C879F1; border-bottom: 0px solid transparent; border-right: 1px solid #C879F1;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:5px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 648px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:1px solid #C879F1; border-bottom:0px solid transparent; border-right:1px solid #C879F1; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div align="center" class="img-container center autowidth fullwidth" style="padding-right: 0px;padding-left: 0px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="center"><![endif]-->
<div style="font-size:1px;line-height:10px"> </div><img align="center" alt="Image" border="0" class="center autowidth fullwidth" src="cid:diveinto.jpeg" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 648px; display: block;" title="Image" width="648"/>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<div class="mobile_hide">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 55px; padding-bottom: 0px; font-family: serif"><![endif]-->
<div style="color:#FFFFFF;font-family:'Merriwheater', 'Georgia', serif;line-height:1.2;padding-top:55px;padding-right:10px;padding-bottom:0px;padding-left:10px;">
<div style="line-height: 1.2; font-family: 'Merriwheater', 'Georgia', serif; font-size: 12px; color: #FFFFFF; mso-line-height-alt: 14px;">
<p style="font-size: 38px; line-height: 1.2; text-align: center; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 46px; margin: 0;"><span style="font-size: 38px;">DIVE INTO RELAX</span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top: 15px; padding-bottom: 0px; font-family: Georgia, 'Times New Roman', serif"><![endif]-->
<div style="color:#FFFFFF;font-family:Georgia, Times, 'Times New Roman', serif;line-height:1.2;padding-top:15px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
<div style="line-height: 1.2; font-family: Georgia, Times, 'Times New Roman', serif; font-size: 12px; color: #FFFFFF; mso-line-height-alt: 14px;">
<p style="line-height: 1.2; text-align: center; font-size: 28px; word-break: break-word; font-family: Georgia, Times, Times New Roman, serif; mso-line-height-alt: 34px; margin: 0;"><span style="font-size: 28px;"><em><span style="color: #00ad99;"><span style="">Enjoy Your Day Spa</span></span></em></span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:transparent;width:650px; border-top: 0px solid transparent; border-left: 1px solid #C879F1; border-bottom: 0px solid transparent; border-right: 1px solid #C879F1;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:55px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 648px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:1px solid #C879F1; border-bottom:0px solid transparent; border-right:1px solid #C879F1; padding-top:5px; padding-bottom:55px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 10px; padding-bottom: 20px; font-family: serif"><![endif]-->
<div style="color:#E3E3E3;font-family:'Merriwheater', 'Georgia', serif;line-height:1.5;padding-top:10px;padding-right:40px;padding-bottom:20px;padding-left:40px;">
<div style="font-size: 12px; line-height: 1.5; font-family: 'Merriwheater', 'Georgia', serif; color: #E3E3E3; mso-line-height-alt: 18px;">
<p style="font-size: 18px; line-height: 1.5; word-break: break-word; text-align: center; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 27px; margin: 0;"><span style="font-size: 18px;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elementum nisl id neque ullamcorper, vel mattis nisl rutrum. Sed pulvinar aliquam dolor et euismod.</span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #3f2765;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:#3f2765;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:#3f2765"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:#3f2765;width:650px; border-top: 0px solid transparent; border-left: 1px solid #C879F1; border-bottom: 0px solid transparent; border-right: 1px solid #C879F1;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:30px; padding-bottom:5px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 648px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:1px solid #C879F1; border-bottom:0px solid transparent; border-right:1px solid #C879F1; padding-top:30px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div align="center" class="img-container center fixedwidth" style="padding-right: 15px;padding-left: 15px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 15px;padding-left: 15px;" align="center"><![endif]-->
<div style="font-size:1px;line-height:15px"> </div><img align="center" alt="Image" border="0" class="center fixedwidth" src="cid:swirlup.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 291px; display: block;" title="Image" width="291"/>
<div style="font-size:1px;line-height:10px"> </div>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 30px; padding-bottom: 30px; font-family: serif"><![endif]-->
<div style="color:#ffffff;font-family:'Merriwheater', 'Georgia', serif;line-height:1.2;padding-top:30px;padding-right:10px;padding-bottom:30px;padding-left:10px;">
<div style="line-height: 1.2; font-family: 'Merriwheater', 'Georgia', serif; font-size: 12px; color: #ffffff; mso-line-height-alt: 14px;">
<p style="line-height: 1.2; text-align: center; font-size: 30px; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 36px; margin: 0;"><span style="font-size: 30px;">TRATAMENTOS</span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid four-up" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #3f2765;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:#3f2765;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:#3f2765"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="162" style="background-color:#3f2765;width:162px; border-top: 0px solid transparent; border-left: 1px solid #C879F1; border-bottom: 0px solid #C879F1; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:25px;"><![endif]-->
<div class="col num3" style="max-width: 320px; min-width: 162px; display: table-cell; vertical-align: top; width: 161px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:1px solid #C879F1; border-bottom:0px solid #C879F1; border-right:0px solid transparent; padding-top:5px; padding-bottom:25px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div align="center" class="img-container center autowidth" style="padding-right: 0px;padding-left: 0px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="center"><![endif]--><img align="center" alt="Alternate text" border="0" class="center autowidth" src="cid:bea_1.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 64px; display: block;" title="Alternate text" width="64"/>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 0px; font-family: Georgia, 'Times New Roman', serif"><![endif]-->
<div style="color:#00ad99;font-family:Georgia, Times, 'Times New Roman', serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:0px;padding-left:10px;">
<div style="line-height: 1.2; font-family: Georgia, Times, 'Times New Roman', serif; font-size: 12px; color: #00ad99; mso-line-height-alt: 14px;">
<p style="line-height: 1.2; text-align: center; font-size: 16px; word-break: break-word; font-family: Georgia, Times, Times New Roman, serif; mso-line-height-alt: 19px; margin: 0;"><span style="font-size: 16px;"><strong><em>Head Massage</em></strong></span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 0px; padding-bottom: 0px; font-family: serif"><![endif]-->
<div style="color:#ffffff;font-family:'Merriwheater', 'Georgia', serif;line-height:1.5;padding-top:0px;padding-right:40px;padding-bottom:0px;padding-left:40px;">
<div style="line-height: 1.5; font-size: 12px; font-family: 'Merriwheater', 'Georgia', serif; color: #ffffff; mso-line-height-alt: 18px;">
<p style="line-height: 1.5; font-size: 34px; text-align: center; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 51px; margin: 0;"><span style="font-size: 34px;">50$</span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 2px solid transparent; width: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td><td align="center" width="162" style="background-color:#3f2765;width:162px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:25px;"><![endif]-->
<div class="col num3" style="max-width: 320px; min-width: 162px; display: table-cell; vertical-align: top; width: 162px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:25px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div align="center" class="img-container center autowidth" style="padding-right: 0px;padding-left: 0px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="center"><![endif]--><img align="center" alt="Alternate text" border="0" class="center autowidth" src="cid:feet.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 64px; display: block;" title="Alternate text" width="64"/>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 0px; font-family: Georgia, 'Times New Roman', serif"><![endif]-->
<div style="color:#00ad99;font-family:Georgia, Times, 'Times New Roman', serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:0px;padding-left:10px;">
<div style="line-height: 1.2; font-family: Georgia, Times, 'Times New Roman', serif; font-size: 12px; color: #00ad99; mso-line-height-alt: 14px;">
<p style="line-height: 1.2; text-align: center; font-size: 16px; word-break: break-word; font-family: Georgia, Times, Times New Roman, serif; mso-line-height-alt: 19px; margin: 0;"><span style="font-size: 16px;"><strong><em>Feet Treatment</em></strong></span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 0px; padding-bottom: 0px; font-family: serif"><![endif]-->
<div style="color:#ffffff;font-family:'Merriwheater', 'Georgia', serif;line-height:1.5;padding-top:0px;padding-right:40px;padding-bottom:0px;padding-left:40px;">
<div style="line-height: 1.5; font-size: 12px; font-family: 'Merriwheater', 'Georgia', serif; color: #ffffff; mso-line-height-alt: 18px;">
<p style="line-height: 1.5; font-size: 34px; text-align: center; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 51px; margin: 0;"><span style="font-size: 34px;">65$</span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 2px solid transparent; width: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td><td align="center" width="162" style="background-color:#3f2765;width:162px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:25px;"><![endif]-->
<div class="col num3" style="max-width: 320px; min-width: 162px; display: table-cell; vertical-align: top; width: 162px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:25px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div align="center" class="img-container center autowidth" style="padding-right: 0px;padding-left: 0px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="center"><![endif]--><img align="center" alt="Alternate text" border="0" class="center autowidth" src="cid:massagstone.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 64px; display: block;" title="Alternate text" width="64"/>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 0px; font-family: Georgia, 'Times New Roman', serif"><![endif]-->
<div style="color:#00ad99;font-family:Georgia, Times, 'Times New Roman', serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:0px;padding-left:10px;">
<div style="line-height: 1.2; font-family: Georgia, Times, 'Times New Roman', serif; font-size: 12px; color: #00ad99; mso-line-height-alt: 14px;">
<p style="line-height: 1.2; text-align: center; font-size: 16px; word-break: break-word; font-family: Georgia, Times, Times New Roman, serif; mso-line-height-alt: 19px; margin: 0;"><span style="font-size: 16px;"><strong><em>Stone massage</em></strong></span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 0px; padding-bottom: 0px; font-family: serif"><![endif]-->
<div style="color:#ffffff;font-family:'Merriwheater', 'Georgia', serif;line-height:1.5;padding-top:0px;padding-right:40px;padding-bottom:0px;padding-left:40px;">
<div style="line-height: 1.5; font-size: 12px; font-family: 'Merriwheater', 'Georgia', serif; color: #ffffff; mso-line-height-alt: 18px;">
<p style="line-height: 1.5; font-size: 34px; text-align: center; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 51px; margin: 0;"><span style="font-size: 34px;">20$</span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 2px solid transparent; width: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td><td align="center" width="162" style="background-color:#3f2765;width:162px; border-top: 0px solid ; border-left: 0px solid ; border-bottom: 0px solid ; border-right: 1px solid #C879F1;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:25px;"><![endif]-->
<div class="col num3" style="max-width: 320px; min-width: 162px; display: table-cell; vertical-align: top; width: 161px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid ; border-left:0px solid ; border-bottom:0px solid ; border-right:1px solid #C879F1; padding-top:5px; padding-bottom:25px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div align="center" class="img-container center autowidth" style="padding-right: 0px;padding-left: 0px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 0px;padding-left: 0px;" align="center"><![endif]--><img align="center" alt="Alternate text" border="0" class="center autowidth" src="cid:face.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 64px; display: block;" title="Alternate text" width="64"/>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top: 10px; padding-bottom: 0px; font-family: Georgia, 'Times New Roman', serif"><![endif]-->
<div style="color:#00ad99;font-family:Georgia, Times, 'Times New Roman', serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:0px;padding-left:10px;">
<div style="line-height: 1.2; font-family: Georgia, Times, 'Times New Roman', serif; font-size: 12px; color: #00ad99; mso-line-height-alt: 14px;">
<p style="line-height: 1.2; text-align: center; font-size: 16px; word-break: break-word; font-family: Georgia, Times, Times New Roman, serif; mso-line-height-alt: 19px; margin: 0;"><span style="font-size: 16px;"><strong><em>Stone massage</em></strong></span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 0px; padding-bottom: 0px; font-family: serif"><![endif]-->
<div style="color:#ffffff;font-family:'Merriwheater', 'Georgia', serif;line-height:1.5;padding-top:0px;padding-right:40px;padding-bottom:0px;padding-left:40px;">
<div style="line-height: 1.5; font-size: 12px; font-family: 'Merriwheater', 'Georgia', serif; color: #ffffff; mso-line-height-alt: 18px;">
<p style="line-height: 1.5; font-size: 34px; text-align: center; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 51px; margin: 0;"><span style="font-size: 34px;">35$</span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 2px solid transparent; width: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #3f2765;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:#3f2765;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:#3f2765"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:#3f2765;width:650px; border-top: 0px solid transparent; border-left: 1px solid #C879F1; border-bottom: 0px solid transparent; border-right: 1px solid #C879F1;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:40px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 648px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:1px solid #C879F1; border-bottom:0px solid transparent; border-right:1px solid #C879F1; padding-top:0px; padding-bottom:40px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<div align="center" class="img-container center fixedwidth" style="padding-right: 15px;padding-left: 15px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 15px;padding-left: 15px;" align="center"><![endif]-->
<div style="font-size:1px;line-height:15px"> </div><img align="center" alt="Image" border="0" class="center fixedwidth" src="cid:swirl.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 291px; display: block;" title="Image" width="291"/>
<div style="font-size:1px;line-height:10px"> </div>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:transparent;width:650px; border-top: 0px solid transparent; border-left: 1px solid #C879F1; border-bottom: 1px solid #C879F1; border-right: 1px solid #C879F1;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 648px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:1px solid #C879F1; border-bottom:1px solid #C879F1; border-right:1px solid #C879F1; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;">
<!--<![endif]-->
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 40px; padding-left: 40px; padding-top: 35px; padding-bottom: 30px; font-family: serif"><![endif]-->
<div style="color:#E3E3E3;font-family:'Merriwheater', 'Georgia', serif;line-height:1.5;padding-top:35px;padding-right:40px;padding-bottom:30px;padding-left:40px;">
<div style="line-height: 1.5; font-size: 12px; font-family: 'Merriwheater', 'Georgia', serif; color: #E3E3E3; mso-line-height-alt: 18px;">
<p style="line-height: 1.5; font-size: 14px; text-align: center; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 21px; margin: 0;"><span style="font-size: 14px;"><span style="font-size: 14px;"><em><span style="color: #00ad99; font-size: 14px;"><strong>Flower Spa</strong></span> </em>- Barkley street, 67 - Seattle</span></span></p>
<p style="line-height: 1.5; font-size: 18px; text-align: center; word-break: break-word; font-family: Merriwheater, Georgia, serif; mso-line-height-alt: 27px; margin: 0;"><span style="font-size: 18px;"><span style="font-size: 14px;">www.example.com | bookings@example.com</span><br/><span style="font-size: 14px;">© All rights reserved </span><br/></span></p>
</div>
</div>
<!--[if mso]></td></tr></table><![endif]-->
<div align="center" class="img-container center autowidth fullwidth" style="padding-right: 15px;padding-left: 15px;">
<!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr style="line-height:0px"><td style="padding-right: 15px;padding-left: 15px;" align="center"><![endif]--><img align="center" alt="Image" border="0" class="center autowidth fullwidth" src="cid:swirls_2.png" style="text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 618px; display: block;" title="Image" width="618"/>
<div style="font-size:1px;line-height:10px"> </div>
<!--[if mso]></td></tr></table><![endif]-->
</div>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<div style="background-color:transparent;">
<div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 650px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;"><tr><td align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:650px"><tr class="layout-full-width" style="background-color:transparent"><![endif]-->
<!--[if (mso)|(IE)]><td align="center" width="650" style="background-color:transparent;width:650px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;" valign="top"><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right: 10px; padding-left: 10px; padding-top:10px; padding-bottom:10px;"><![endif]-->
<div class="col num12" style="min-width: 320px; max-width: 650px; display: table-cell; vertical-align: top; width: 650px;">
<div style="width:100% !important;">
<!--[if (!mso)&(!IE)]><!-->
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:10px; padding-bottom:10px; padding-right: 10px; padding-left: 10px;">
<!--<![endif]-->
<div class="mobile_hide">
<table border="0" cellpadding="0" cellspacing="0" class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 10px; padding-right: 10px; padding-bottom: 10px; padding-left: 10px;" valign="top">
<table align="center" border="0" cellpadding="0" cellspacing="0" class="divider_content" height="15" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid transparent; height: 15px; width: 100%;" valign="top" width="100%">
<tbody>
<tr style="vertical-align: top;" valign="top">
<td height="15" style="word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</div>
<!--[if (!mso)&(!IE)]><!-->
</div>
<!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>
<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
</td>
</tr>
</tbody>
</table>
<!--[if (IE)]></div><![endif]-->
</body>
</html>"""
            msgText = MIMEText(message, 'html')
            msgRoot.attach(msgText)

            images = [
                ["./images/bea_1.png", "<bea_1.png>"],
                ["./images/diveinto.jpeg", "<diveinto.jpeg>"],
                ["./images/face.png", "<face.png>"],
                ["./images/feet.png", "<feet.png>"],
                ["./images/logoflower.png", "<logoflower.png>"],
                ["./images/massagstone.png", "<massagstone.png>"],
                ["./images/swirl.png", "<swirl.png>"],
                ["./images/swirls_1.png", "<swirls_1.png>"],
                ["./images/swirls_2.png", "<swirls_2.png>"],
                ["./images/swirlup.png", "<swirlup.png>"]
            ]

            for image in images:
                with open(image[0],'rb') as f:
                    msgImage = MIMEImage(f.read())
                    f.close()
                msgImage.add_header('Content-ID', image[1])
                msgRoot.attach(msgImage)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msgRoot)
                smtp.quit()

            
            credentials = pickle.load(open("./token.pkl","rb"))

            service = build("calendar","v3",credentials=credentials)

            id = service.calendarList().list().execute()['items'][0]['id']

            event = {
            'summary': 'Horário marcado '+c_nome,
            'location': endereco,
            'description': 'Horário marcado com '+c_nome+' para '+p_nome+'.',
            'start': {
                'dateTime': date.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': "America/Sao_Paulo",
            },
            'end': {
                'dateTime': (date + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': "America/Sao_Paulo",
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'email', 'minutes': 60},
                {'method': 'popup', 'minutes': 30},
                ],
            },
            }

            event = service.events().insert(calendarId=id, body=event).execute()
