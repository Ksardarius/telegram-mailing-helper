<div class="u-container-layout u-container-layout-2" id="dispatch-group-buttons">
    %for info in dispatchGroupNames:
    <a style="width: 100%" href="#" id="dispatch_group_button_{{info.id}}"
       onclick="getGroupInfo('{{info.id}}')"
       class="u-border-5 {{'u-border-green' if info.enabled else 'u-border-red'}} u-btn u-btn-round u-button-style u-hover-black u-none u-radius-9 u-text-black u-text-hover-white u-btn-1">{{info.dispatch_group_name}}</a>
    %end
</div>