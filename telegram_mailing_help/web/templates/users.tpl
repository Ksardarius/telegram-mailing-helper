<!DOCTYPE html>
<html style="font-size: 16px;">
% include('web/templates/header.tpl', title='Disp: Пользователи', custom_css='users.css')
    <section class="u-align-center u-clearfix u-section-1" id="sec-2267">
      <div class="u-clearfix u-sheet u-valign-top u-sheet-1">
        <div class="u-expanded-width u-table u-table-responsive u-table-1">
          <table class="u-table-entity u-table-entity-1">
            <colgroup>
                <col width="5%">
                <col width="19%">
                <col width="19%">
                <col width="19%">
                <col width="19%">
                <col width="19%">
            </colgroup>
            <thead class="u-black u-table-header u-table-header-1">
              <tr style="height: 21px;">
                <th class="u-border-1 u-border-black u-table-cell">#ID</th>
                <th class="u-border-1 u-border-black u-table-cell">TgId</th>
                <th class="u-border-1 u-border-black u-table-cell">Пользователь</th>
                <th class="u-border-1 u-border-black u-table-cell">Состояние</th>
                <th class="u-border-1 u-border-black u-table-cell">Действия</th>
                <th class="u-border-1 u-border-black u-table-cell">Добавлен</th>
              </tr>
            </thead>
            <tbody class="u-table-alt-grey-5 u-table-body">
            % for user in users:
              <tr style="height: 21px;">
                <td class="u-border-1 u-border-grey-30 u-first-column u-grey-50 u-table-cell u-table-cell-5">{{user.id}}</td>
                <td class="u-border-1 u-border-grey-30 u-first-column u-table-cell u-table-cell-5">{{user.telegram_id}}</td>
                <td class="u-border-1 u-border-grey-30 u-first-column u-table-cell u-table-cell-5">{{user.name}}</td>
                <td class="u-border-1 u-border-grey-30 u-table-cell" id="user_state_{{user.id}}">{{userStateCls(user.state).getLocalizedMessage()}}</td>
                <td class="u-border-1 u-border-active-palette-2-base u-border-hover-palette-1-base u-btn-rectangle u-none u-table-cell u-text-palette-1-base u-table-cell-7">
                  <a href="#a" onclick="changeUserState('{{user.id}}')" class="u-active-none u-border-none u-btn u-button-link u-button-style u-hover-none u-none u-text-palette-1-base u-btn-1">  Изменить состояние</a>
                </td>
                <td class="u-border-1 u-border-grey-30 u-table-cell">{{user.created}}</td>
              </tr>
            % end
            </tbody>
          </table>
        </div>
      </div>
    </section>
% include('web/templates/footer.tpl')
