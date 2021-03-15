from src.dynamo_db import get_user_info, Language

_en = {
    'Monday': 'Mon',
    'Tuesday': 'Tue',
    'Wednesday': 'Wed',
    'Thursday': 'Thu',
    'Friday': 'Fri',
    'Saturday': 'Sat',
    'Sunday': 'Sun',
    'options:choose': 'Choose an option',
    'button:help:clockin': 'Clock In/Out',
    'button:help:report': 'Report',
    'button:help:edit': 'Editing entries',
    'button:help:deleteall': 'Data deletion',
    'button:help:issue': 'Report issue',
    'button:delete_all': 'Delete all data',
    'button:help': 'Help',
    'button:edit': 'Edit entry',
    'button:source': 'Source code',
    'button:other': 'Another',
    'button:today': 'Today',
    'button:yesterday': 'Yesterday',
    'button:report:week': 'Week',
    'button:report:month': 'Month',
    'button:report:last_week': 'Last week',
    'button:report:last_month': 'Last month',
    'button:clock_inout': 'Clock In/Out',
    'button:report': 'Report',
    'button:options': 'Options',
    'button:yes': 'Yes',
    'button:no': 'No',
    'feedback:entrance': "Entry registered!",

    'feedback:exit': 'Exit registered!\n'
                     'Please reply to this message telling what you did during this period.',

    'feedback:exit:insist_reply': 'You haven\'t answered me yet with a description of what you did in the last '
                                  'period.\n'
                                  'Please reply to this message with a brief description of what you have done.',

    'feedback:exit:acknowledgment': 'Description received :) Thanks!',

    'report:period:choose': 'Choose a period for the report',
    'report:choice:empty': 'There are no records for the selected period',
    'report:choice:too_many_chars': 'The report is too big, I am sending it to you as a regular text file',
    'report:description:not_found': 'No description',
    'report:total_of_day': 'Total of the day',
    'report:total_of_period': 'Total of the selected period',
    'language:choose': 'Choose your preferred language /\nEscolha a sua língua preferida',
    'language:set': 'Hi! :) \nThis bot will help you keep track of your work time in the simplest possible way.',
    'timezone:request': 'Please inform your region so we can set your timezone information.\n'
                        'Any good reference of your place is sufficient like "state of michigan" or "new york".',
    'timezone:location:not_found': 'Gosh, unfortunately I could not find your location. Could you please try again '
                                   'using another description of your region?',
    'timezone:location:confirm': 'I\'ve found this timezone for you.\n'
                                 '{}'
                                 'Do you wish to keep this configuration?',
    'setup:complete': 'Great! Now that everything is set, let me explain how I work.'
                      '\n- When you begin to work, press the square button in the typing field to open my custom '
                      'keyboard. Then, press the "Clock In/Out" button to register your entry. When you stop/pause '
                      'your work time, press that button again and I\'ll detect and register it as a "clock out".  Be '
                      'aware that after a "clock out" event you\'ll only be able to input new commands after sending '
                      'a brief message stating what you\'ve worked on during that period, this will be useful later. '
                      '\n\n- At some point you\'ll need to know on what you spent your time on. This is when '
                      'you can use the other button in the special keyboard: the "reports" button. You will be prompted'
                      ' to select a period for the report. This is why knowing your timezone is important!'
                      '\n\nHope you enjoy my services! '
                      '\nFor questions/suggestions and the source code: https://github.com/herzog0/TimeTrackingBot',
    'error:generic': 'Hmm, I didn\'t understand what you did',
    'delete:confirm': 'Attention!\n'
                      'This will delete all your data from my database.\n'
                      'Are you sure you want to proceed?\n'
                      'This operation is  irreversible.',
    'delete:success': 'All your information has been deleted.',
    'delete:cancelled': 'Ok, I won\'t delete anything.',
    'delete:nothing': 'You have nothing to be deleted.',
    'start:prohibit': 'Sorry, you can\'t do that right now.\n'
                      'You have a pending issue and need to resolve this before resetting your information.\n'
                      'Try to clock in/out and see the suggested instructions!',
    'default': 'Sorry, I didn\'t understand what you said. If you need help use the command /help',
    'request:start': 'Please, type the command /start.',
    'request:missing_entry': 'Please, reply this message with the missing entry in the format:\nhh:mm\n<description>',
    'request:warning': 'regx*xAttention!regx*x You forgot to register your exit in the following day: ',
    'request:acknowledgment': 'Thank you. Now you can try to clock in again.',
    'edit:choose:message': 'regx*xYou are entering manual edit mode!regx*x\n'
                           'This feature is only useful for you if you want to change entry times and '
                           'descriptions.\n'
                           'In case you forgot to clock out yesterday you regx*xdon\'tregx*x need to be in '
                           'edit mode. Just try to clock in now and I\'ll ask you to insert yesterday\'s end time.\n'
                           'If you want to proceed, press one of the buttons below with the day you wish to edit. ',
    'edit:request_day': 'Ok, you have chosen to edit the entries of another day.\n'
                        'Please, send me the day you want to edit in the following format:\n'
                        'regx*xdd/mm/yyyyregx*x\n'
                        '(or, send /cancel to exit the edit mode)',
    'edit:request:date:wrong_format': 'You sent the date in the wrong format.\n'
                                      'Please, send it in the following format:',
    'edit:request:entry:wrong_format': 'You sent the entry in the wrong format.\n'
                                       'Please, send it in the following format:',
    'edit:request:date_model': 'regx*xdd/mm/yyyyregx*x',
    'edit:suggest:cancel': '(or, send /cancel to exit the edit mode)',
    'edit:request:empty': 'No entries were found on the selected day. Since you are in edit mode, you can send me '
                          'the entries and descriptions of the day so that it can be filled out.',
    'edit:request:not_empty': 'The above message is a compilation of the entries you made in the  chosen day to edit.\n'
                              'Copy the message and paste it in your typing field. Make the transformations '
                              'you want and send me the result.',
    'edit:request:instructions:1': 'Pay regx*xcloseregx*x attention to the format of the entries, they must follow '
                                   'exactly this model:',
    'edit:request:instructions:2': 'The above model may be inserted how many times you wish to, as long as they\'re '
                                   'all in the same message and in chronological order.',
    'edit:request:validation_error': 'Edit validation error.\n'
                                     'Please, send the entries in the format:',
    'edit:request:model': '<entry time in hh:mm>\n'
                          '<exit time in hh:mm>\n'
                          '<obligatory description>\n'
                          '<blank line>',
    'edit:incomplete_day': 'You can only edit days that have pairs of entries and exits. There is a missing checkout '
                           'on the date you selected',
    'edit:done': 'regx*xEdit done!regx*x\nYou can check the changes by requesting a report for that day.',
    'validator:clockin': 'Clock In',
    'validator:clockout': 'Clock Out',
    'source': 'To report an issue, see the soruce code, contribute or solicit a feature, visit the project in '
              'https://github.com/herzog0/TimeTrackingBot',
    'cancelled': 'Operation cancelled',
    'help': 'Which function do you want help with?',
    'help:clockin': 'regx*x/clockinregx*x\n'
                    'To use this command, send it manually or use the button in the special '
                    'keyboard accessible by the square icon in your typing field.\n'
                    'With this command you will let me know if a period of your workday has started or ended. Just use '
                    'it once when entering and again when leaving or pausing.\n'
                    'In case you forgot to let me know when you left work the other day, don\'t worry, I will '
                    'demand it from you when you try to clock in again. If that\'s not enough, you can always use '
                    'the regx*x/editregx*x command to edit a day\'s entries.\n'
                    'Also, every time you use this command and I recognize it as an exit or pause event, '
                    'I will ask you for a brief description of what you did in that period. You must send it in a '
                    'single message in response to the request message I sent (touch my message and select "Reply").\n'
                    'To find out how much time you have counted with the entries, use the command regx*x/reportregx*x.',
    'help:report': 'regx*x/reportregx*x\n'
                   'To use this command, send it manually or use the button in the special '
                   'keyboard accessible by the square icon in your typing field.\n'
                   'With this command you will be able to request reports of your time spent in work. '
                   'You can request reports for different periods. '
                   'Be aware of the fact that I keep your records up to a maximum of 2 months after insertion. '
                   'That is, if you hit the spot on the 1st of any month, you can request a report containing that '
                   'entry until the last day of the following month. After that the obsolete records will be deleted '
                   'automatically.',
    'help:edit': 'regx*x/editregx*x\nTo use this command, send it manually or use the "Options" menu button '
                 'accessible by the square icon in your typing field.\n'
                 'With this command you will be able to request to edit the entries of some day of work, as well as '
                 'the descriptions of each period.',
    'help:deleteall': 'regx*x/deleteregx*x\nTo use this command, send it manually or use the "Options" menu button '
                      'accessible by the square icon in your typing field.\n'
                      'With this command you will be able to request the deletion of absolutely all your data from '
                      'my database.\n'
                      'To save your time records (and other important information for my operation) I use a database '
                      'managed by Amazon Web Services. If you are concerned about your privacy, this command will '
                      'cause all your records to be deleted from my database, with no possibility of recovery. In '
                      'addition, my code is open to anyone who wants to see and contribute :)',
    'help:issue': 'If you have noticed a bug in my system, please notify the project maintainer in the "Issues" '
                  'section through the link https://github.com/herzog0/TimeTrackingBot.',
}

_pt = {
    'Monday': 'Seg',
    'Tuesday': 'Ter',
    'Wednesday': 'Qua',
    'Thursday': 'Qui',
    'Friday': 'Sex',
    'Saturday': 'Sáb',
    'Sunday': 'Dom',
    'options:choose': 'Escolha uma opção',
    'button:help:clockin': 'Ponto',
    'button:help:report': 'Relatório',
    'button:help:edit': 'Edição de entradas',
    'button:help:deleteall': 'Deleção dos dados',
    'button:help:issue': 'Reportar problema',
    'button:delete_all': 'Apagar tudo',
    'button:help': 'Ajuda',
    'button:edit': 'Editar ponto',
    'button:source': 'Código fonte',
    'button:other': 'Outro',
    'button:today': 'Hoje',
    'button:yesterday': 'Ontem',
    'button:report:week': 'Semana',
    'button:report:month': 'Mês',
    'button:report:last_week': 'Semana passada',
    'button:report:last_month': 'Mês passado',
    'button:clock_inout': 'Ponto',
    'button:report': 'Relatório',
    'button:options': 'Opções',
    'button:yes': 'Sim',
    'button:no': 'Não',
    'feedback:entrance': 'Entrada registrada!',

    'feedback:exit': 'Saída registrada!\n'
                     'Responda essa mensagem dizendo o que fez você durante esse período, por favor.',

    'feedback:exit:insist_reply': 'Você ainda não me respondeu com uma descrição do que fez no último período.\n'
                                  'Por favor, responda essa mensagem com uma breve descrição do que você fez.',

    'feedback:exit:acknowledgment': 'Descrição recebida :) Obrigado!',

    'report:period:choose': 'Escolha um período para o relatório',
    'report:choice:empty': 'Não há registros para o período selecionado',
    'report:choice:too_many_chars': 'O relatório é grande demais, estou lhe enviando como um arquivo de texto comum',
    'report:description:not_found': 'Sem descrição',
    'report:total_of_day': 'Total do dia',
    'report:total_of_period': 'Total do período selecionado',
    'language:choose': 'Choose your preferred language /\nEscolha a sua língua preferida',
    'language:set': 'Olá! :) \nEstou aqui para te ajudar a manter controle das suas horas de trabalho da forma mais '
                    'simples possível.',
    'timezone:request': 'Por favor, informe sua região para que possamos configurar seu fuso horário.\n'
                        'Qualquer boa referência da sua localização será suficiente, como "estado de são paulo" ou '
                        '"cidade de são roque".',
    'timezone:location:not_found': 'Puxa, infelizmente não pude encontrar sua localização. Poderia tentar novamente '
                                   'usando outra descrição da sua região?',
    'timezone:location:confirm': 'Encontrei esse fuso horário para você.\n'
                                 '{}'
                                 'Gostaria de manter essa configuração?',
    'setup:complete': 'Ótimo! Agora que tudo está configurado deixe-me explicar como eu funciono.'
                      '\n- Quando você começar a trabalhar, pressione o botão quadrado no campo de digitação para '
                      'abrir meu teclado especial. Então, pressione o botão "Ponto" para registrar sua entrada. Quando '
                      'você for fazer uma pausa ou parar de trabalhar, pressione esse botão novamente e eu detectarei '
                      'este registro como uma interrupção. Esteja ciente de que após um evento de interrupção você só '
                      'poderá usar novos comandos depois que me enviar uma breve descrição do que você fez durante '
                      'aquele período, isso será útil mais tarde.'
                      '\n\n- Em algum momento você precisará saber no que você gastou o seu tempo. Aqui você poderá '
                      'usar o outro botão no teclado especial: o botão de "relatórios". Você será solicitado a '
                      'selecionar um período para o relatório. Por isso que é importante eu saber seu fuso horário!'
                      '\n\nEspero que você goste dos meus serviços! '
                      '\nPara dúvidas/sugestões e o código fonte: https://github.com/herzog0/TimeTrackingBot',
    'error:generic': 'Hmm, eu não entendi o que você fez',
    'delete:confirm': 'Atenção! Isso irá apagar todos os seus dados salvos na minha base.\nTem certeza de que '
                      'deseja prosseguir?\nEsta operação é irreversível.',
    'delete:success': 'Todas as suas informações foram excluídas.',
    'delete:cancelled': 'Ok, não irei apagar nada.',
    'delete:nothing': 'You have nothing to be deleted.',
    'start:prohibit': 'Desculpe, você não pode fazer isso agora.\n'
                      'Você está com alguma pendência e precisa resolver isso antes de redefinir suas informações.\n'
                      'Tente bater um ponto e ver as instruções sugeridas!',
    'default': 'Desculpe, não entendi o que você disse. Caso precise de ajuda use o comando /help',
    'request:start': 'Please, type the command /start.',
    'request:missing_entry': 'Por favor, responda essa mensagem com a entrada faltando no formato:\nhh:mm\n<descrição>',
    'request:warning': 'regx*xAtenção!regx*x Você esqueceu de registrar sua saída no dia: ',
    'request:acknowledgment': 'Obrigado. Agora você pode tentar bater o ponto novamente.',
    'edit:choose:message': 'regx*xVocê está entrando no modo de edição manual!regx*x\n'
                           'Esta funcionalidade só é útil para você caso queira alterar horários ou descrições de hoje '
                           'ou de dias passados.\n'
                           'Caso você tenha esquecido de bater o ponto final no dia de ontem você regx*xnãoregx*x '
                           'precisa do modo de edição. Basta tentar bater o ponto novamente agora que eu irei te '
                           'pedir para inserir o horário final de ontem.\n'
                           'Caso queira prosseguir, pressione um dos botões abaixo com o dia que você deseja editar.',
    'edit:request_day': 'Ok, você escolheu editar os registros de outro dia.\n'
                        'Por favor, me envie a data que deseja editar no seguinte formato:\n'
                        'regx*xdd/mm/yyyyregx*x\n'
                        '(ou, envie /cancel para sair do modo de edição)',
    'edit:request:date:wrong_format': 'Você enviou a data no formato errado.\n'
                                      'Por favor, envie no formato:',
    'edit:request:entry:wrong_format': 'Você enviou o registro no formato errado.\n'
                                       'Por favor, envie no formato:',
    'edit:request:date_model': 'regx*xdd/mm/yyyyregx*x',
    'edit:suggest:cancel': '(ou, envie /cancel para sair do modo de edição)',
    'edit:request:empty': 'Nenhuma entrada foi encontrada no dia selecionado. Como você está no modo de edição, você '
                          'pode me enviar as entradas e descrições do dia para que ele seja preenchido.',
    'edit:request:not_empty': 'A mensagem acima é uma compilação dos registros que você fez no dia selecionado para '
                              'edição.\n'
                              'Copie a mensagem e cole-a no seu campo de digitação. Faça as transformações que desejar '
                              'e me envie o resultado.',
    'edit:request:instructions:1': 'Preste regx*xmuitaregx*x atenção ao formato das entradas, elas precisam seguir '
                                   'exatamente este modelo:',
    'edit:request:instructions:2': 'O modelo acima pode ser inserido quantas vezes desejar, desde que estejam todos '
                                   'na mesma mensagem e em ordem cronológica.',
    'edit:request:validation_error': 'Erro na validação da edição.\n'
                                     'Por favor, envie as entradas no formato:',
    'edit:request:model': '<horário de entrada em hh:mm>\n'
                          '<horário de saída em hh:mm>\n'
                          '<descrição obrigatória>\n'
                          '<linha em branco>\n'
                          '(repetições...)',
    'edit:incomplete_day': 'Você só pode editar dias que possuem pares de entradas e saídas. Existe um registro de '
                           'saída faltante na data que você selecionou',
    'edit:done': 'regx*xEdição feita!regx*x\nVocê pode verificar as alterações requisitando um relatório daquele dia.',
    'validator:clockin': 'Entrada',
    'validator:clockout': 'Saída',
    'source': 'Para reportar um problema, ver o código fonte, contribuir ou solicitar funcionalidades, visite o '
              'projeto em https://github.com/herzog0/TimeTrackingBot.',
    'cancelled': 'Operação cancelada',
    'help': 'Você quer ajuda para qual função?',
    'help:clockin': 'regx*x/pontoregx*x\nPara usar este comando, envie-o manualmente ou use o botão no '
                    'teclado especial acessível pelo ícone quadrado no seu campo de digitação.\n'
                    'Com este comando você irá me informar se começou ou terminou um período da sua jornada de '
                    'trabalho. Basta usá-lo uma vez na hora de entrar e outra vez na hora de sair ou pausar.\n'
                    'Caso você tenha esquecido de me avisar quando saiu do trabalho em outro dia, não se preocupe, eu '
                    'vou cobrar isso de você quando tentar bater o ponto novamente. Se isso não não for suficiente, '
                    'você sempre pode usar o comando regx*x/editarregx*x para editar as entradas de um dia '
                    'específico.\n'
                    'Além disso, toda vez que você bater um ponto e eu reconhecê-lo como um evento de saída ou pausa, '
                    'vou te solicitar uma breve descrição do que fez naquele período. Você deve enviá-la em uma única '
                    'mensagem como resposta à mensagem de solicitação que mandei (toque na minha mensagem e selecione '
                    '"Reponder").\n'
                    'Para saber quanto tempo você tem contabilizado com os pontos, use o comando '
                    'regx*x/relatorioregx*x.',
    'help:report': 'regx*x/relatorioregx*x\nPara usar este comando, envie-o manualmente ou use o botão no '
                   'teclado especial acessível pelo ícone quadrado no seu campo de digitação.\n'
                   'Com este comando você poderá solicitar relatórios sobre o tempo despendido em trabalho junto com '
                   'as descrições providas em cada período. Você pode solicitar relatórios para diversos períodos. '
                   'Esteja atento ao fato de que guardo seus registros até no máximo 2 meses após sua inserção. '
                   'Ou seja, se você bater o ponto no dia 1 de algum mês, você poderá solicitar um relatório contendo '
                   'essa entrada até o último dia do mês seguinte. Após isso os registros obsoletos serão excluídos '
                   'automaticamente.',
    'help:edit': 'regx*x/editarregx*x\nPara usar este comando, envie-o manualmente ou use o botão menu "Opções" '
                 'acessível pelo ícone quadrado no seu campo de digitação.\n'
                 'Com este comando você poderá solicitar a edição das entradas de algum dia de trabalho, assim como '
                 'as descrições de cada período.',
    'help:deleteall': 'regx*x/apagarregx*x\nPara usar este comando, envie-o manualmente ou use o botão menu "Opções" '
                      'acessível pelo ícone quadrado no seu campo de digitação.\n'
                      'Com este comando você poderá solicitar a deleção de absolutamente todos os seus dados do meu '
                      'banco de dados.\n'
                      'Para guardar seus registros de ponto (e outras informações importantes para meu funcionamento) '
                      'uso um banco de dados gerenciado pela Amazon Web Services. Caso você esteja preocupado com a '
                      'sua privacidade, este comando fará com que todos os seus registros sejam apagados da minha '
                      'base, sem nenhuma possibilidade de recuperação. Além disso, o meu código é aberto para quem '
                      'quiser ver e contribuir :)',
    'help:issue': 'Caso tenha notado algum bug em meu sistema, por favor avise o mantenedor do projeto na seção '
                  '"Issues" através do link https://github.com/herzog0/TimeTrackingBot.',
}
_strings = _en


def strings():
    return _strings


def set_strings(*, chat_id: str = None, force_lang: Language = None):
    if force_lang is not None:
        lang = force_lang
    else:
        try:
            lang = Language(get_user_info(chat_id)['lang'])
        except KeyError:
            lang = Language('en')

    if lang == Language.PORTUGUESE:
        global _strings
        _strings = _pt


bla = ""

if __name__ == '__main__':
    print(set(_en.keys()) == set(_pt.keys()))
