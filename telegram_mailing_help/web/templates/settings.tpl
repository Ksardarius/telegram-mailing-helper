<!DOCTYPE html>
<html style="font-size: 16px;">
  % include('header.tpl', title='Disp: Настройки', custom_css='settings.css')
    <section class="u-align-center u-clearfix u-section-1" id="sec-2267">
      <div class="u-clearfix u-sheet u-valign-top u-sheet-1">
        <div class="u-expanded-width u-table u-table-responsive u-table-1">
          <table class="u-table-entity u-table-entity-1">
            <colgroup>
              <col width="20%">
              <col width="40%">
              <col width="40%">
            </colgroup>
            <thead class="u-black u-table-header u-table-header-1">
              <tr style="height: 21px;">
                <th class="u-border-1 u-border-black u-table-cell">Ключ</th>
                <th class="u-border-1 u-border-black u-table-cell">Описание</th>
                <th class="u-border-1 u-border-black u-table-cell">Значение</th>
              </tr>
            </thead>
            <tbody class="u-table-alt-grey-5 u-table-body">
            % for setting in settings:
              <tr style="height: 21px;">
                <td class="u-border-1 u-border-grey-30 u-first-column u-table-cell u-table-cell-5"><a href="#a" onclick="changeSettings('{{setting.key}}')">{{setting.key}}</a></td>
                <td class="u-border-1 u-border-grey-30 u-first-column u-table-cell u-table-cell-5">{{setting.description}}</td>
                <td id="settings-{{setting.key}}" class="u-border-1 u-border-grey-30 u-first-column u-table-cell u-table-cell-5">{{setting.value}}</td>
              </tr>
            % end
            </tbody>
          </table>
        </div>
      </div>
    </section>
  % include('footer.tpl')
